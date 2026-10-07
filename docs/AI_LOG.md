# AI-assisted development log

Prepared at Prompt 03, 2026-10-07, Asia/Singapore. Current user: M3 - Magos. AI tool: Codex in the current desktop chat. This log records available evidence; it is not proof of member understanding or authored Git history.

## Recording policy

Keep actual prompts and relevant responses, the member responsible, evaluations of correctness/suitability/limitations, code adaptations, verification, and commit/PR links. Do not expose secrets. Full chat transcript export/share link is currently pending; the records below distinguish verbatim prompt blocks, verbatim response excerpts, and summaries. A prepared prompt alone is not evidence that it was used.

Human evaluation fields stay pending until Magos provides their own judgment. Assistant evaluation and generated modifications below are labeled as such. No work is attributed to Agbas or Daro without actual evidence.

## Earlier planning context

Before the numbered prompts, Magos requested reading the Practical Exam, sample UI, and photographed checklist without starting implementation; then requested a persistent plan and a five-field, stage-by-stage Markdown prompt guide. These are summaries of the current chat, not a transcript reproduction. Outputs: EXAM_PLAN.md and BUILD_PROMPTS.md. The shared rules call for original styling, required features first, and truthful records.

## AI-01 - Requirements planning

- Date: 2026-10-07; precise message timestamp not exported.
- Responsible requester: Magos (identity supplied later in the same chat).
- Type: analysis/planning; no app generation, debugging, or refactoring claim.
- Prompt: five-field Prompt 01 was actually pasted by the user; reproduced below from its matching guide block.
- Relevant response excerpt (verbatim): "Prompt 01 is complete. I updated EXAM_PLAN.md with the scope, architecture, requirement mapping, proposed member tasks, and remaining gaps. Only this planning document changed."
- Response summary: required seven-step flow, F01-F20 and A-F evidence, proposed Django/Tailwind/SQLite/session design, optional-feature exclusions, and genuine member tasks/gaps.
- Assistant evaluation: scope matches reviewed exam functionality; group identity/access/contributions were unresolved and not marked verified.
- Assistant adaptation: added mapping tables and a small genuine-task proposal to EXAM_PLAN.md.
- Human evaluation / adaptations: Pending Magos's own account of what was checked, accepted, or changed.
- Verification: planning mappings inspected; no runtime checks were claimed.
- Commit/PR: None created by this stage; files remained uncommitted.

## AI-02 - Original design and data proposal

- Date: 2026-10-07; precise message timestamp not exported.
- Responsible requester: Magos.
- Type: planning/design; no screens or models implemented.
- Prompt: five-field Prompt 02 was actually pasted; reproduced below. Supplementary supplied facts: instructor Reban Cliff A. Fajardo, MIT; repo https://github.com/Yray0-9/pos-app; M1 Agbas, M2 Daro, M3 Magos.
- Relevant response excerpt (verbatim): "Prompt 02's proposal is complete." (Typography normalized from the rendered response.)
- Response summary: DESIGN.md with Common Table, cream/green/plum, six products and expected calculations, product grid above full-width order list, feedback/accessibility states, snapshots, Decimal calculations, guarded transitions, duplicate handling, and reset isolation.
- User's actual acceptance response: "Accept the proposed direction".
- User identity/deadline response (verbatim): "I am magos and also about the deadline will be later 9pm so now we should follow the instructions."
- Assistant evaluation: design differs from sample UI; text color pairs were calculated, but no actual screens or accessibility compliance were claimed.
- Assistant adaptation: recorded acceptance and user facts in DESIGN.md and EXAM_PLAN.md; reference prices and layout remain independent of the sample UI.
- Human critical evaluation / code adaptation: Pending. Acceptance alone is not a detailed correctness/limitation evaluation.
- Verification: document mapping and calculated solid-color contrast only; app behavior remained pending.
- Commit/PR: None created.

## AI-03 - Reproducible foundation and evidence records

- Date: 2026-10-07, approximately 11:49-11:55 Asia/Singapore for setup checks; record completion time can be added when exported.
- Responsible requester: Magos.
- Type: setup generation and verification.
- Prompt: five-field Prompt 03 was pasted twice, with the first tool sequence interrupted. The second submission added the Acceptance Checklist PDF and permission to correct BUILD_PROMPTS.md. Its five-field text is reproduced below.
- Supplementary instruction (verbatim): "About this file build_prompts.md you can change anything because this is your building so it is okay to be mistake as long as it is so not critical."
- Supplementary attachment request: user supplied IT415 Acceptance Checklist.pdf and asked for it to be read properly. The request is summarized here; full transcript export is pending.
- Response/action record: inspected existing Python 3.14.4 / Django 6.1.2, read all 4 new PDF pages, installed python-dotenv 1.2.4 after an authorized network retry, replaced the hard-coded secret with environment configuration, created safe ignore/dependency/template/initializer files and evidence records, expanded README, and corrected the prompt workflow for branches before feature editing.
- Assistant evaluation: dotenv avoids writing a custom environment parser; actual versions are pinned. Missing secrets fail clearly, local initialization preserves existing files, and private files are ignored. A local HTTP 200 proves scaffold startup only; it does not satisfy kiosk functionality.
- Assistant-generated adaptations: settings load an ignored .env with process-variable precedence, localhost-only development hosts, and Asia/Singapore display time. A private fresh key is generated locally without logging it. No kiosk app or migration was created.
- Verification: actual check commands/results and expected secret failure in TEST_RESULTS.md, S01-S19. Initial package network denial was an environment/tool limitation. A verification helper's shell-quoting error was corrected in scratch code; neither is presented as a kiosk application bug-fix stage.
- Human evaluation / personally applied changes: Pending Magos. Suggested questions: Why is .env ignored? Why is DEBUG development-only? What does manage.py check prove? Why is the welcome page not a working kiosk?
- Actual code/record files: pos_app/settings.py; requirements.txt; .gitignore; .env.example; scripts/init_env.py; README.md; docs/AI_LOG.md; docs/MEMBER_REGISTER.md; docs/TEST_RESULTS.md; updates to EXAM_PLAN.md and BUILD_PROMPTS.md.
- Commit/PR: None made; local setup changes remain uncommitted on main.

## Debugging and refactoring evidence still needed

No genuine kiosk application error or meaningful application refactor has occurred because kiosk features do not exist yet. When one occurs, preserve the real error/original code, actual prompt/response, applied fix/improvement, and verification. Do not invent a bug or deliberately degrade code for the checklist.

## Entry template for later stages

```text
Date/time and milestone:
Responsible member and actual GitHub identity:
AI tool:
Requirement IDs:
Actual prompt / response or accessible evidence reference:
Original error/code when relevant:
Assistant analysis (labeled):
Member evaluation: correctness, suitability, limitations:
Member changes/adaptations and reason:
Verification: exact action, expected result, observed result:
Files, actual commit SHA, feature branch, PR source/target:
Reviewer, feedback resolution, merge/integration revision:
Pending evidence:
```

## Actual five-field prompts used in this chat

The following blocks will be populated from the matching saved prompts. Supplemental facts/changes are noted above. Full assistant responses are still in the current chat; only labeled excerpts/summaries are recorded in this file so far.

### AI-01 - verbatim five-field prompt

```text
Context:
We are preparing a three-member IT415 touchscreen POS kiosk exam. I have a newly generated Django project and currently expect to do the implementation myself with AI assistance. Read docs/BUILD_PROMPTS.md's shared rules and docs/EXAM_PLAN.md. The sample UI is only a behavioral reference.

Objectives:
Finalize the minimum complete scope and explain how we will cover both the application requirements and development checklist before coding.

Requirements:
Map the campus-outlet problem, users, inputs, outputs, and seven-step transaction flow to F01-F20 and checklist sections A-F. Separate mandatory work from optional features. Propose Django templates, modest JavaScript, Tailwind CSS, and a simple storage approach, with reasons. Identify genuine tasks the other members could implement, review, verify, document, and explain; distinguish implementation contributions from supporting tasks that do not satisfy the feature-branch requirement. Record my stated role honestly. Ask concisely for missing deadline, member names/accounts, and separately issued professor rules; continue independent planning while answers are pending.

Constraints:
Planning only: no application code, dependencies, migrations, Git mutations, or server changes. Do not claim that one person and AI satisfy every member requirement. Keep unresolved instructor questions visible without blocking independent planning.

Expected output:
An updated EXAM_PLAN.md with scope and collaboration gaps, a clear explanation of the required flow, and the proposed architecture. End at this planning milestone; identify Prompt 02 as next.
```

### AI-02 - verbatim five-field prompt

```text
Context:
Our requirements plan is ready. Apply the shared rules in docs/BUILD_PROMPTS.md and review docs/EXAM_PLAN.md. We want a modern, calm kiosk with Tailwind, without reproducing the professor's sample UI.

Objectives:
Choose a coherent original visual direction and a simple data/state design before implementation.

Requirements:
Prepare docs/DESIGN.md with a proposed original store name, six or more products and prices, a distinct layout, restrained palette, typography, spacing, and consistent controls. Map item selection, review, payment choices, cash/QR/card states, success, receipt, and reset. Include empty, error, loading, focus, and success states. Aim for touch targets at least 48 CSS pixels, readable contrast, keyboard access, and responsive tablet/desktop behavior. Explain a recommendation for SQLite product and completed-sale records plus a session-based active cart. Define decimal money, trusted server calculations, sale-item snapshots, unique references, allowed transitions, duplicate-payment handling, and isolation of consecutive customers. Explain that clearing the active receipt does not require deleting historical sale records.

Constraints:
Design and planning only; do not implement screens or models. Do not add login, inventory, reports, or a separate frontend framework. Product choices and the layout are our own. Distinguish proposed design decisions from professor requirements.

Expected output:
DESIGN.md, agreed/proposed data decisions in EXAM_PLAN.md, and a concise walkthrough I can understand. Make the design concrete enough for review before Prompt 03; do not silently treat unresolved preferences as approved.
```

### AI-03 - verbatim five-field prompt

```text
Context:
We have a Django scaffold and a reviewed scope/design. Read the shared rules, EXAM_PLAN.md, DESIGN.md, and the actual repository state.

Objectives:
Prepare a reproducible development foundation and evidence records without building kiosk features yet.

Requirements:
Check the existing virtual environment and installed Django version; run the relevant Django configuration check and resolve setup issues within this stage. Record actual dependencies in the project's dependency file. Add an appropriate .gitignore for the virtual environment, caches, local database, environment files, and generated artifacts. Establish secret configuration suitable for sharing without exposing current values. Create AI_LOG.md, MEMBER_REGISTER.md, and TEST_RESULTS.md with truthful initial records and pending fields. Extend README with verified environment/setup/run instructions and current limitations. Inspect branch, remote configuration, and untracked files without exposing credentials; explain how we will preserve the scaffold in genuine history. Record prior planning prompts accurately where accessible.

Constraints:
No cart, payment, models, or UI features yet. Do not recreate the project, overwrite unrelated work, commit, push, or merge. Do not invent member names, dependency versions, successful startup, or retrospective evidence.

Expected output:
A checked foundation, dependency and ignore files, initial evidence documents, and README instructions. Explain the Django project versus app distinction and report actual checks. Identify Prompt 04 and the separate Git checkpoint prompt where appropriate.
```

## AI-GIT-01 - Authorized setup checkpoint

- Date: 2026-10-07, approximately 12:00-12:06 Asia/Singapore.
- Responsible requester: M3 - Magos. Authenticated account and configured Git author: Yray0-9; configured authorship was preserved.
- User actually invoked the five-field reusable B prompt reproduced below.
- Assistant actions/results: reviewed 17 scoped foundation/scaffold/evidence files; confirmed local-secret and original hard-coded-secret exclusion; Django/pip checks passed; remote main matched the initial commit; authenticated account had push permission; no existing setup PR was found.
- Actual branch: codex/setup-foundation, created for this checkpoint after the earlier non-Git setup stage.
- Actual setup commit: [a20201aeb262959b4d38f5f80bed78a3b5e8d56f](https://github.com/Yray0-9/pos-app/commit/a20201aeb262959b4d38f5f80bed78a3b5e8d56f).
- Push: succeeded to origin/codex/setup-foundation, tracking configured.
- Actual PR: [#1](https://github.com/Yray0-9/pos-app/pull/1), source codex/setup-foundation -> target main; author Yray0-9; open and unmerged.
- Review evidence: API review list was empty at verification. No reviewer message/assignment, feedback, merge, or deployment occurred. Genuine teammate reviewer account still needed.
- Assistant adaptation: updated README/plan/register/guide and this log with actual links in a subsequent documentation commit on the same branch. This is evidence maintenance, not a claim of an extra application stage.
- Human evaluation/explanation: Pending Magos. Other members' individual accounts/feature contributions/explanations remain pending.
- Verification limits: local diff and configuration/dependency checks; no new kiosk functionality or fresh-clone demonstration claimed. The separate full instructor checklist remains pending.

### AI-GIT-01 - verbatim five-field prompt used

```text
Context:
We have completed and checked the current kiosk milestone. Apply the shared rules in docs/BUILD_PROMPTS.md and inspect the actual repository, current branch/PR, and MEMBER_REGISTER.md. I want this milestone recorded in Git and prepared for review now.

Objectives:
Preserve real incremental history and provide a concrete review PR for this milestone.

Requirements:
Review the diff and checks. Preserve unrelated user changes and credentials. Use a suitable feature branch with the codex/ prefix unless an agreed member branch already applies; use configured authorship without impersonation. Commit only the milestone and relevant evidence with a meaningful message, push to the confirmed intended repository, and create/update a scoped PR identifying source/target branches, behavior, and actual validation. Attach the PR to this chat. Record actual commit/branch/PR links and member responsibility. Identify the real reviewer needed, source of feedback, and unresolved member-contribution gaps. If a review has occurred, address the actual feedback and record its resolution; never invent review.

Constraints:
No force pushes, fabricated history, merging, or deployment. Do not send messages to a reviewer without my explicit instruction. If remote access or required information is missing, complete the local reviewable work and explain what remains.

Expected output:
A genuine scoped commit and review PR when access permits, evidence links, checks, and remaining review requirements. Return to the next numbered build stage; do not merge automatically.
```
