"""Check public-profile validation and rendering without private source files."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from build import ROOT, build, load_profile, render


class BuildTests(unittest.TestCase):
    def write_profile(self, root, profile):
        (root / 'profiles').mkdir(exist_ok=True)
        (root / 'profiles/default.json').write_text(json.dumps(profile))

    def test_projection_and_regeneration_without_private_files(self):
        profile = load_profile(ROOT)
        artifacts = render(profile)
        self.assertEqual(set(artifacts), {Path('skills/vael/SKILL.md'), Path('skills/vael/agents/openai.yaml')})
        skill = artifacts[Path('skills/vael/SKILL.md')]
        for pref in profile['preferences']:
            self.assertEqual(pref['instruction'] in skill, pref['enabled'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            instructions = '# Development instructions\n'
            (root / 'AGENTS.md').write_text(instructions)
            self.write_profile(root, profile)
            self.assertEqual(build(root), artifacts)
            self.assertEqual(build(root), artifacts)
            self.assertEqual((root / 'AGENTS.md').read_text(), instructions)
            self.assertFalse((root / 'analysis').exists())
            self.assertFalse((root / 'generated').exists())
            for relative, content in artifacts.items():
                self.assertEqual((ROOT / relative).read_text(), content)

    def test_disabling_preference_removes_instruction(self):
        profile = copy.deepcopy(load_profile(ROOT))
        pref = profile['preferences'][0]
        pref['enabled'] = False
        for content in render(profile).values():
            self.assertNotIn(pref['instruction'], content)

    def test_private_metadata_and_legacy_schema_rejected(self):
        for field in ('session_id', 'text_sha256', 'evidence', 'supporting_interactions', 'global_default'):
            for level in ('root', 'preference'):
                with self.subTest(field=field, level=level), tempfile.TemporaryDirectory() as directory:
                    profile = copy.deepcopy(load_profile(ROOT))
                    target = profile if level == 'root' else profile['preferences'][0]
                    target[field] = 'not for publication'
                    root = Path(directory)
                    self.write_profile(root, profile)
                    with self.assertRaisesRegex(ValueError, 'Unexpected'):
                        load_profile(root)
        for version in (1, 2):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                profile = copy.deepcopy(load_profile(ROOT))
                profile['schema_version'] = version
                root = Path(directory)
                self.write_profile(root, profile)
                with self.assertRaisesRegex(ValueError, 'schema'):
                    load_profile(root)

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = copy.deepcopy(load_profile(ROOT))
            profile['preferences'].append(copy.deepcopy(profile['preferences'][0]))
            root = Path(directory)
            self.write_profile(root, profile)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                load_profile(root)

    def test_weak_signal_requires_review_before_enabling(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = copy.deepcopy(load_profile(ROOT))
            next(p for p in profile['preferences'] if p['classification'] == 'weak')['enabled'] = True
            root = Path(directory)
            self.write_profile(root, profile)
            with self.assertRaisesRegex(ValueError, 'Review weak'):
                load_profile(root)


if __name__ == '__main__':
    unittest.main()
