# Developing Vael

Vael is a local-first personal engineering configuration project. This file governs development of Vael; the generated skill lives in `skills/vael/`.

- Keep `profiles/default.json` as the source of truth for reviewed preferences. Preserve applicable contexts and exceptions. Confidence labels are author assessments, not public empirical claims.
- Public profile schema version 3 deliberately excludes conversation evidence, counts, timestamps, session identifiers, hashes, and source paths. Keep private research outside the repository.
- Keep user-designed task modes separate from reviewed preferences. Their source is the template in `scripts/build.py`.
- Change generated instructions through the profile or renderer, then rebuild. Keep the installed skill self-contained.
- Use Python's standard library. Add dependencies and infrastructure only for demonstrated requirements.
- Never add private history, credentials, caches, or personal machine configuration. Ignore rules are a precaution, not permission to retain private material in the public tree.
- Do not install skills, replace global instructions, commit, push, or publish implicitly as part of a build.
- Run `python3 -B scripts/build.py` and `python3 -B scripts/test_build.py` after relevant changes.
