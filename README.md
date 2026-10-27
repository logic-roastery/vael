# Vael

A Codex skill for discussing, reviewing, designing, and implementing software with clear scope and deliberate changes.

Vael asks the agent to follow project conventions, compare working implementations, preserve behavior during migrations, and verify relevant changes. Commits and pushes stay with you unless you explicitly authorize them.

## Install

### From GitHub

Ask Codex:

```text
Use $skill-installer to install the vael skill from
https://github.com/logic-roastery/vael/tree/main/skills/vael
into ~/.agents/skills.
```

Only `skills/vael/` is installed. You do not need Python or the rest of this repository to use the skill.

After installation, type `$vael` in Codex. If it does not appear, restart Codex and check `/skills`.

### From a local checkout

For developing or customizing Vael, link the skill to your checkout. Run these commands from the repository root:

```sh
mkdir -p "$HOME/.agents/skills"
if [ -e "$HOME/.agents/skills/vael" ] || [ -L "$HOME/.agents/skills/vael" ]; then
  printf '%s\n' 'Vael is already installed. Review that installation before replacing it.'
else
  ln -s "$PWD/skills/vael" "$HOME/.agents/skills/vael"
fi
```

Codex supports symlinked skill folders. Changes to the generated skill in this checkout become available through the link. Keep the checkout in place while using it.

For use in just one project, copy `skills/vael/` into that project's `.agents/skills/` instead. Choose one installation method to avoid duplicate copies. See the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and installation locations.

## Use Vael

| Mode | Use it for | File edits |
|---|---|---|
| Discuss | Explain behavior, explore an idea, compare options | None |
| Review | Find actionable problems in code or a proposed change | None |
| Architecture | Assess boundaries, dependencies, data flow, and trade-offs | None |
| Update | Implement an authorized change and verify the result | Within the requested scope |

```text
$vael discuss: should this logic live in the service or a shared component?
$vael review: inspect this branch for bugs and unnecessary changes. Do not edit.
$vael architecture: assess this polling design and compare it with our existing pattern.
$vael update: implement option B and run the relevant tests. Do not commit.
```

You can switch modes naturally. After a discussion, “implement option B” authorizes implementation while retaining the agreed scope. Explicit restrictions such as “don't update” still apply. Debugging can use any of the four modes.

A request for a commit message does not authorize a commit. If you want the agent to commit or push, say so explicitly.

## Update or remove an installation

**Linked installation:** update your checkout using your normal Git workflow. If you change the profile or renderer, rebuild the skill as described below.

**Copied or installer-managed installation:** review the new version and back up any edits made directly to your installed copy. Remove that copy, then repeat the GitHub installation. The built-in installer stops when the destination already exists; it does not overwrite it in place.

To uninstall from the user-level location used in this guide:

```sh
rm -r "$HOME/.agents/skills/vael"
```

This removes the installed folder or symlink. It leaves a linked source checkout intact. For a project-only installation, remove that project's `.agents/skills/vael` instead.

## Customize and build

Maintainers need Python 3 with its standard library. No additional packages, API keys, or private conversation files are required.

1. Edit `profiles/default.json` to change a preference, its contexts, or its exceptions. Set `enabled` to `false` to exclude it from the skill.
2. Edit the template in `scripts/build.py` to change mode behavior or the generated UI metadata.
3. Rebuild and run the checks from the repository root:

```sh
python3 -B scripts/build.py
python3 -B scripts/test_build.py
```

The build writes `skills/vael/SKILL.md` and `skills/vael/agents/openai.yaml`. Direct edits to those files will be replaced on the next build. A linked installation sees the rebuilt files; a copied installation needs to be refreshed.

The profile uses schema version 3. Preserve its existing fields and allowed classifications. Weak or one-time preferences require review and reclassification before they can be enabled. Confidence labels are author assessments, not publicly reproducible measurements.

## Project files

```text
profiles/default.json            Editable preferences
scripts/build.py                Skill and metadata generator
scripts/test_build.py           Profile validation and build checks
skills/vael/SKILL.md              Generated skill instructions
skills/vael/agents/openai.yaml    Generated Codex UI metadata
AGENTS.md                       Instructions for maintaining this repository
```

Install the skill folder, not the repository's root `AGENTS.md`.

## Troubleshooting

| Problem | What to check |
|---|---|
| `$vael` is missing | Confirm the installed folder contains `SKILL.md`. Check `/skills`, then restart Codex if needed. |
| Old or duplicate instructions appear | Check for other Vael copies in user-level and project-level skill directories, including an older installation under `~/.codex/skills/`. Keep the intended copy. |
| Profile changes do not appear | Run the build. If the installation is a copy, refresh it after rebuilding. |
| The build rejects a preference | Check schema version, field names, duplicate IDs, classification, and confidence against the existing profile. |
