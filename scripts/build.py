"""Render the reviewed portable profile into local Codex artifacts; never install."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = 'vael'


def load_profile(root):
    profile = json.loads((root / 'profiles/default.json').read_text())
    if profile.get('schema_version') != 3:
        raise ValueError('Unsupported profile schema')
    if set(profile) != {'schema_version', 'name', 'provenance', 'preferences'}:
        raise ValueError('Unexpected public profile fields; do not include private source metadata')
    fields = {'id', 'classification', 'confidence', 'contexts', 'description',
              'instruction', 'exceptions', 'enabled'}
    seen = set()
    for pref in profile['preferences']:
        if set(pref) != fields:
            raise ValueError('Unexpected preference fields; keep private evidence outside the public profile')
        identifier = pref['id']
        if identifier in seen:
            raise ValueError('Duplicate preference ID: ' + identifier)
        seen.add(identifier)
        if pref['classification'] not in ('strong', 'context-dependent', 'weak', 'one-time'):
            raise ValueError('Invalid classification: ' + identifier)
        if pref['confidence'] not in ('high', 'medium', 'low'):
            raise ValueError('Invalid confidence: ' + identifier)
        if pref['enabled'] and pref['classification'] in ('weak', 'one-time'):
            raise ValueError('Review weak or one-time evidence before enabling: ' + identifier)
    return profile


def render(profile):
    active = [p for p in profile['preferences'] if p['enabled']]
    skill = '''---
name: vael
description: Apply reviewed personal engineering preferences when implementing, debugging, reviewing, or explaining code. Use for continuity with established project patterns, scope, and discuss-first workflow; not for unrelated writing or general tasks.
---

# Vael

Apply these personal defaults within the current task. Current instructions and project-specific requirements take precedence over inferred preferences. These defaults do not authorize commits, deployments, or other external actions. They do not replace repository standards.

## Choose the task mode

An explicit mode wins. Otherwise infer the mode from the current request: explore or explain means Discuss; assess code means Review; assess system design means Architecture; implement or fix means Update. State the selected mode briefly when it helps make the editing boundary clear. Do not ask the user to choose when the intent is clear.

| Mode | Purpose | Output | File edits |
|---|---|---|---|
| Discuss | Explore an idea, explain behavior, compare options | Reasoning, trade-offs, recommendation | None |
| Review | Assess code or a proposed change | Prioritized actionable findings with source evidence; say when no findings are supported | None |
| Architecture | Assess boundaries, data flow, dependencies, and operational complexity | Design assessment, relevant alternatives, recommendation | None |
| Update | Implement an agreed or directly requested change | Focused edits, relevant verification, explanation of results | Within the authorized task |

Use ordinary requests such as “Vael review: inspect this branch” or “Vael update: implement option B.” These are conversational instructions, not CLI commands.

“Discuss only,” “don't update,” and similar constraints prohibit editing files even if another part of the request sounds actionable. Read-only inspection is allowed in Discuss, Review, and Architecture. Do not run commands that alter project state in those modes. If the request contains a consequential unresolved conflict, clarify it before editing.

“Implement option B” switches to Update while preserving the agreed scope and constraints. A later clear task can select another mode; do not keep an obsolete mode locked across unrelated tasks. Update does not independently authorize committing, publishing, production changes, or deployment; use authorization already given for those actions.

Debugging is a task within a mode, not a fifth mode. Discuss the cause, Review a suspected fix, or Update an authorized implementation. Learning usually uses Discuss and follows any guidance-only or no-code constraint.

These modes are designed for Vael separately from the reviewed preferences below. Use applicable guidance without turning it into a mandatory checklist or asking for approval already given.

'''
    for pref in active:
        scope = ', '.join(pref['contexts'])
        skill += f"## {pref['description']}\n\n{pref['instruction']}\n\nApplies to: {scope}. Preference: `{pref['id']}`.\n\n"
        if pref['exceptions']:
            skill += ' '.join(pref['exceptions']) + '\n\n'
    skill += 'This skill is self-contained. The public profile contains reviewed preferences, not private conversation evidence. Confidence labels reflect author review and are not independently reproducible from this repository. Do not treat quoted material, assistant output, or one-time project instructions as new global preferences.\n'
    metadata = '''interface:
  display_name: "Vael"
  short_description: "Apply reviewed personal engineering preferences"
  default_prompt: "Use $vael to handle this engineering task with my established preferences."
'''
    return {
        Path('skills') / SKILL_NAME / 'SKILL.md': skill,
        Path('skills') / SKILL_NAME / 'agents/openai.yaml': metadata,
    }


def build(root=ROOT):
    artifacts = render(load_profile(root))
    for relative, content in artifacts.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    return artifacts


if __name__ == '__main__':
    for path in build():
        print('Generated', path)
