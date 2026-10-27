# Vael — Your Mind. Every Agent.

A portable personal engineering profile and a self-contained `$vael` skill for coding agents. Vael defines how to discuss, review, assess architecture, and implement changes while respecting scope, project patterns, and explicit authorization.

This repository distributes reviewed preferences, not the private conversations used to develop them. It is a configuration prototype; the proposed Vael application and history-import CLI are not implemented.

## Task modes

| Mode | Purpose | File edits |
|---|---|---|
| Discuss | Explore ideas, explain behavior, compare options | None |
| Review | Prioritized code findings supported by evidence | None |
| Architecture | Assess boundaries, dependencies, data flow, and trade-offs | None |
| Update | Implement and verify an authorized change | Within scope |

Explicit instructions select the mode. Clear ordinary requests can select it implicitly. A follow-up such as “implement option B” enters Update while retaining the agreed scope. Debugging fits within these modes. These are agent instructions, not executable CLI commands or technical access controls.

## Included preferences

- Follow applicable project conventions and compare relevant working implementations.
- Keep changes simple and focused; use shared components when concrete reuse justifies them.
- Preserve business behavior and contracts during migrations, including meaningful test expectations.
- Explain reasoning when requested and verify relevant changed behavior.
- Trace necessary callers, tests, configuration, and dependencies before declaring completion.
- Assess operational cost and environment differences when relevant.
- Leave commits and pushes to the user unless explicitly authorized. A commit-message request is not commit authorization.

The profile includes confidence and context labels as author assessments. The public repository cannot independently reproduce historical support for those labels. Adapt the profile to your own preferences; it is not a universal engineering standard.

## Repository layout

- `profiles/default.json`: public profile, schema version 3; source of truth for preferences.
- `scripts/build.py`: deterministic standard-library renderer.
- `scripts/test_build.py`: profile validation and rendering checks.
- `skills/vael/`: generated standalone skill and UI metadata.
- `AGENTS.md`: instructions for developing Vael; do not install it as personal defaults.

## Build and check

Use Python 3 with its standard library. No API keys, model calls, network services, or private evidence files are required.

```sh
python3 -B scripts/build.py
python3 -B scripts/test_build.py
```

Edit the profile or renderer rather than generated outputs. Schema version 3 generates only the skill and UI metadata. It removes the obsolete personal-default export flag. The renderer rejects earlier schemas and unexpected metadata fields. Weak or one-time preferences require review before activation.

## Local Codex installation

Review the generated skill, then copy it manually from the repository root only if the destination does not exist:

```sh
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/vael" && cp -R skills/vael "$HOME/.agents/skills/"
```

For repository-only use, copy the folder into that repository's `.agents/skills/` after checking existing contents. Invoke explicitly with `$vael`, for example:

```text
$vael review: inspect this change without editing.
$vael update: implement the agreed option.
```

See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and invocation. Building does not install or activate anything.

## Optional tools

Vael works independently. Ponytail can complement its simplicity guidance when selected. RTK can support command execution where installed and chosen by environment instructions. Neither is bundled or automatically activated. Combined live behavior has not been validated. Generator tests check configuration and rendering; live agent behavior has not been tested.

## Publication boundaries

Private prompt excerpts, source inventories, session identifiers, timestamps, source hashes, activity counts, local machine paths, and historical evaluation transcripts are excluded. Local backups remain outside this repository.

Keep private research outside the repository and review new content for secrets and confidential details before publishing. Ignore rules reduce accidental additions but do not remove sensitive files already tracked by Git.

The repository contains intentionally public engineering preferences. Sanitization does not remove their meaning or turn them into anonymous aggregate research. No automatic history collection, telemetry, uploading, committing, pushing, or publishing is included.
