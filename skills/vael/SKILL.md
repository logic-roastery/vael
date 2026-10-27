---
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

## Keep work within the requested feature or branch changes.

Keep changes focused on the requested feature or branch diff. Avoid unrelated renaming, configuration edits, and cleanup; expand scope only when needed to complete the task, and explain the dependency.

Applies to: implementation, review, debugging. Preference: `engineering.scope`.

Necessary callers, tests, and configuration remain in scope.

## Inspect and reuse the surrounding project patterns before introducing a new approach.

Inspect comparable working code and applicable project conventions before choosing an implementation. Check a relevant sibling service when it is available and useful; explain material differences before adapting its approach. Reuse established naming and patterns, and justify new mechanisms with concrete requirements.

Applies to: implementation, review, architecture. Preference: `engineering.project-patterns`.

Company-specific conventions apply only in their projects. Existing patterns do not justify a demonstrated correctness or security defect. Inspect sibling projects read-only within available access; do not broaden the implementation scope or copy an incompatible pattern.

## Prefer understandable, minimal implementations over unnecessary mechanisms.

Choose the simplest complete solution. Question redundant branches, extra files, and abstractions without a demonstrated purpose. Reuse or generalize when concrete use cases justify it; avoid speculative flexibility. Preserve necessary validation and reliability.

Applies to: implementation, review, architecture. Preference: `engineering.simplicity`.

This is not a permanent ban on helper methods, locks, entity graphs, or events. Concrete reuse can justify a shared wrapper without justifying a general framework.

## Respect explicit inspection, discussion, and guidance-only requests.

When asked to inspect, assess, discuss, or explain first, provide findings or guidance without editing files. A guide-only request may also exclude sample code. Once implementation is authorized, proceed within that scope without repeating the approval question.

Applies to: implementation, review, learning, architecture. Preference: `workflow.task-mode`.

Do not turn this into an approval gate on every implementation task. The current user request determines the mode.

## Explain why and compare behavior when understanding or decision support is requested.

For explanations and technical decisions, connect the recommendation to this codebase, explain why it works, and compare old and new behavior or relevant alternatives. Increase detail when the user asks for deeper understanding.

Applies to: learning, architecture, explanation. Preference: `communication.explain-reasoning`.

No evidence supports always-long or always-short answers. Do not produce code in guidance-only mode when the user excluded it.

## Check relevant tests and be clear about whether they actually passed.

After implementation, run checks relevant to the changed behavior when available. Report what ran, whether it passed, and any untested behavior. Add tests for missing behavior coverage rather than test volume alone.

Applies to: implementation, debugging. Preference: `verification.relevant-tests`.

This profile does not require universal test-first development. A passing suite alone does not prove coverage; add checks for actual gaps.

## Preserve business behavior and contracts during migrations and structural changes.

During migrations and structural changes, preserve business behavior, response and error contracts, and unaffected positive and negative test expectations. Explain intentional behavior changes and why any assertions change; do not change expectations merely to make tests pass.

Applies to: implementation, refactoring. Preference: `engineering.behavior-continuity`.

Implement behavior changes explicitly requested by the user and fix demonstrated defects. Equivalent assertions may be adapted to a new API or test framework when the same contract remains covered.

## Investigate the cause and relevant request evidence before recommending a fix.

For debugging, inspect the failing path and available request or log evidence, explain the cause, and distinguish confirmed findings from hypotheses before proposing a targeted fix.

Applies to: debugging. Preference: `debugging.root-cause`.

Do not imply access to production telemetry that is unavailable.

## Leave commits and pushes to the user unless explicitly authorized.

Complete authorized edits and verification, but leave commits and pushes to the user unless explicitly requested. A request for a commit message does not authorize committing. When asked, provide a message specific to the current changes, separated by repository when relevant.

Applies to: implementation. Preference: `workflow.user-commits`.

Explicit authorization to commit or push overrides this default within its stated scope. Do not ask again for authorization already given.

## Naming should be deliberate and consistent, including test names.

Use descriptive names consistent with the project, including affected tests, and avoid incidental renames.

Applies to: implementation, review. Preference: `engineering.naming`.

Exact identifier choices and operator restrictions from individual projects are not portable global rules.

## Check whether shared components already own the responsibility.

Before duplicating logic in an application, check whether an existing shared component, starter, or workflow already provides or should own it. Recommend the appropriate boundary and justify extraction with concrete reuse.

Applies to: architecture, implementation, review. Preference: `engineering.shared-ownership`.

Do not automatically move code into a shared module or change another repository. Confirm the relevant consumers and compatibility first.

## Trace the necessary impact of a change before declaring it complete.

Trace necessary changes through callers, tests, configuration, and affected services. Report remaining dependencies or rollout steps and identify unaffected behavior where relevant; do not declare end-to-end completion from a local check alone.

Applies to: implementation, review, architecture. Preference: `workflow.change-completeness`.

Keep the investigation proportional to the task. Identifying an affected service does not authorize editing or deploying it.

## Consider cost, request volume, and environment behavior for operational changes.

For logging, polling, scheduler, or infrastructure changes, assess relevant effects on cost, request volume, and environment-specific behavior. Distinguish measured evidence from estimates and preserve the intended differences between environments.

Applies to: architecture, review, implementation, debugging. Preference: `operations.change-impact`.

This is not a mandatory operational audit for every edit. Do not claim savings or performance improvements without evidence.

This skill is self-contained. The public profile contains reviewed preferences, not private conversation evidence. Confidence labels reflect author review and are not independently reproducible from this repository. Do not treat quoted material, assistant output, or one-time project instructions as new global preferences.
