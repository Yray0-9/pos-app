# IT415 POS kiosk: prompts from planning to demonstration

Prepared: 2026-10-07 (Asia/Singapore).

## How to use this guide

Copy **one numbered prompt's entire text block** into this chat at a time. Let that stage finish, read the explanation, and resolve its failures before moving to the next. The guide prepares future work; creating this file does not start implementation.

Current checkpoint: Prompt 03 setup is committed/pushed on codex/setup-foundation; [PR #1](https://github.com/Yray0-9/pos-app/pull/1) is open into main with genuine review and merge pending. Before editing the next feature, invoke reusable E to establish its actual contributor's branch, then use Prompt 04. E must account for the unmerged setup dependency safely; do not discard or silently merge it. Use B after each real milestone and C only after actual review/checks. Do not wait until the entire app is finished to record history.

New source reviewed: `IT415 Acceptance Checklist.pdf` (4 pages). It requires at least seven real development stages in committed history, one shared repository, actual member/PR evidence, and individual verification. Deleted merged branches may be evidenced through their PRs/commits. See MEMBER_REGISTER.md for the working matrix; do not treat pending as P or N/A.

Every prompt uses the professor's five fields: **Context, Objectives, Requirements, Constraints, Expected output**. Prompts 01-02 make decisions without implementing features. Later prompts perform only their stated milestone. Do not paste this entire file as one build request.

`docs/EXAM_PLAN.md` is the requirement checklist. Keep it, this guide, and the evidence records in the project so work can continue across chats. The original PDFs and checklist image remain the assignment sources. If a source cannot be accessed later, say so and use the reviewed plan provisionally; do not invent its contents.

### Shared rules for every prompt

These rules are part of each prompt below:

- Read applicable repository instructions, `docs/EXAM_PLAN.md`, and existing code before changing anything. Respect completed work and update stale assumptions.
- Build only the requested stage. Explain its purpose in plain language, then finish and verify that stage. Stop before the next stage; do not repeatedly ask permission for routine changes already within the requested scope.
- Keep the design original and modern, with calm colors, clear typography, ample spacing, and touch-friendly controls. Do not copy the professor's sample branding, layout, palette, or assets.
- Prefer Django templates, locally built Tailwind CSS, SQLite if agreed, and small amounts of JavaScript. Check actual installed versions and current official documentation when needed. Do not invent package versions or install extra frameworks without a reason.
- Prioritize required functions over inventory, discounts, login, reports, real payments, or other optional features. No real money, card details, or payment credentials are needed.
- Keep an honest AI log: prompt/response records or accessible references, responsible member, evaluation, adaptations, verification, and limitations. Separate AI analysis from the human member's own evaluation. Unknown identities and human explanations stay pending.
- Update checklist items only after verifying their pass conditions. Report unrun checks and unresolved failures accurately. Use meaningful tests for calculations, validation, state transitions, and data consistency; visual review covers appearance.
- Preserve user changes. Do not commit, push, open a PR, merge, deploy, or submit work solely because this guide mentions those actions. Use the separate Git prompt when explicitly invoked. Never fabricate branches, authorship, reviews, errors, test results, or member contributions.
- Before future feature editing, use reusable E or explicitly authorize that branch preparation. Keep setup, interface, core functionality, validation, a genuine bug fix, a genuine refactor, and documentation represented as real stages; do not manufacture problems/commits to reach seven.
- Our group has three members. I currently expect to implement the project personally with AI assistance. This does not establish contributions from the other two members or satisfy the checklist's individual requirements. Keep those gaps visible and help identify genuine work they can perform or questions to clarify with the professor. Do not send messages to anyone without my explicit instruction.
- End each stage with what changed, how it was verified, what I should understand or try myself, any pending evidence, and the next prompt number. Do not claim the whole exam is complete while requirements remain pending.

### Evidence files to maintain starting in Prompt 03

| File | Purpose |
| --- | --- |
| `docs/EXAM_PLAN.md` | Requirement status, decisions, and remaining gaps |
| `docs/AI_LOG.md` | Actual prompts/responses, evaluation, adaptations, debugging and refactoring |
| `docs/MEMBER_REGISTER.md` | Real member accounts, tasks, branches, commits, PRs, reviews, and merges |
| `docs/TEST_RESULTS.md` | Checks performed, expected/observed results, failures, dates, and tested revision/state |
| `docs/DESIGN.md` | Original design and interaction decisions |

These files now exist after Prompt 03. Records distinguish observed checks from pending evidence and labeled summaries from complete responses. Use safe excerpts and references; do not record secrets or virtual-environment contents. Do not place a whole assistant-written evaluation under a member's name and treat it as their understanding.

## Prompt 01 - Confirm scope, requirements, and honest collaboration plan

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

## Prompt 02 - Agree on original design and data behavior

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

## Prompt 03 - Verify setup and create development evidence records

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

## Prompt 04 - Build the original UI foundation with Tailwind

```text
Context:
Setup is verified and evidence documents exist. Apply the shared rules and the decisions in EXAM_PLAN.md and DESIGN.md. First confirm that branch preparation was performed through reusable E (or equivalent explicit authorization) before changing UI files. If it was not authorized, inspect and explain the missing checkpoint without mutating Git or implementing feature files yet.

Objectives:
Create the reusable visual foundation for our original kiosk, without implementing transaction features yet.

Requirements:
Create the kiosk Django app and route if needed. Configure a reproducible local Tailwind build using actual supported tooling, Django-template content detection as required by the installed version, and documented commands. The evaluation app should use built local CSS without requiring a CDN connection. Build a base template with our agreed original branding, navigation/progress treatment, readable typography, touch controls, accessible feedback components, and responsive spacing. Preview the foundation in a browser when available and inspect overflow, focus visibility, and CSS loading. Record verified results and design decisions.

Constraints:
Use Django templates and modest JavaScript; no unnecessary React/Vue framework. Do not copy sample UI assets or layout. No pretend working payment buttons or full transaction implementation. Keep decorative animation subtle and respect reduced motion.

Expected output:
A functioning styled base page, Tailwind configuration/build scripts, README build instructions, and an explanation of template/static-file responsibilities. Report visual checks accurately and stop before Prompt 05.
```

## Prompt 05 - Implement catalog and transaction data foundations

```text
Context:
Our UI foundation works. Apply the shared rules and the storage/state decisions in DESIGN.md and EXAM_PLAN.md.

Objectives:
Implement the data foundation needed for accurate orders and completed transactions.

Requirements:
Implement the agreed product, completed transaction, and transaction-item structures using SQLite if that decision was accepted. Use Decimal for prices and payment amounts, distinct transaction references, payment-method values, timestamp, and product/price snapshots on completed items. Provide a repeatable way to seed at least six agreed products without duplication. Plan shared calculation and completion responsibilities so all payment methods can use the same trusted logic. Apply required migrations and verify seeded values and relevant money/reference behavior. Explain why cart state and completed-sale records have different lifetimes.

Constraints:
No inventory, public administration features, reports, or real payment gateway. Do not delete an existing database or rewrite migrations already applied elsewhere. Do not implement all payment flows in this stage. Avoid unnecessary abstractions.

Expected output:
Verified models/migrations or the agreed alternative, repeatable sample data, updated evidence, and an explanation of each stored field. Stop before Prompt 06.
```

## Prompt 06 - Implement product selection and cart controls

```text
Context:
Catalog/data and the original UI foundation are ready. Apply shared rules and F01-F06 plus applicable F02/F20 requirements.

Objectives:
Build a working touch-friendly selection screen and current order.

Requirements:
Display at least six product cards with visible names and prices. Tapping adds an item. Implement increase, decrease, and explicit removal; define zero quantity clearly and never allow negative or invalid quantities. Show name, unit price, quantity, subtotal, and total. Calculate from trusted product data on the server and preserve the cart in the agreed session storage. Provide an empty state and helpful feedback. Prevent checkout for an empty cart as our correctness decision. Verify multiple additions, repeated product selection, quantity changes, removal, invalid inputs, and arithmetic with the agreed catalog.

Constraints:
No payment processing or completed receipts yet. Do not trust browser-submitted prices/totals. Avoid fragile UI-only state and full-page complexity that prevents simple touch use. Do not mark order-review requirements complete yet.

Expected output:
A working selection/cart milestone, meaningful verification results, evidence updates, and a simple explanation of subtotal and total calculation. Stop before Prompt 07.
```

## Prompt 07 - Implement review and preserved navigation

```text
Context:
Product selection and cart operations are verified. Apply shared rules and F07-F08, F02, and F20.

Objectives:
Let customers review the exact order and return to editing without losing it.

Requirements:
Add an order summary showing every product, quantity, unit price, subtotal, and total. Provide clear Back and Continue to Payment controls. Back must preserve selections and quantities. Continuing must reflect the current server-validated cart; an empty cart cannot advance. Keep navigation and styling consistent with DESIGN.md. Verify agreement between selection and summary, modifications after going Back, and repeated navigation. Define behavior if a stored cart references a missing or unavailable product.

Constraints:
Do not implement payment completion yet. No duplicate total-calculation logic. Do not freeze an outdated amount while the order is still editable or discard items on ordinary Back navigation.

Expected output:
A verified review flow, evidence updates, and an explanation of how cart state survives navigation. Stop before Prompt 08.
```

## Prompt 08 - Implement payment choices and validated cash payment

```text
Context:
Selection and review work. Apply shared rules and F09-F12 plus the consistency requirements in F15.

Objectives:
Build payment-method selection and a correct cash-payment flow.

Requirements:
Provide large Cash, QR Payment, and Credit/Debit Card choices. Implement Cash with amount due, amount-paid input, Pay Now, clear errors, and automatic change calculation. Provide touch-friendly entry without requiring a desktop keyboard. Reject blank, nonnumeric, non-finite, negative, and insufficient values; define a sensible two-decimal currency policy. Keep rejected payments on the payment screen and create no successful transaction or receipt. Accept exact and excess payment. Use shared completion logic to create a completed sale only after validation, capture the actual order snapshot, and prevent repeated submission from creating another sale. Clear or recompute stale payment state if the customer edits the order. Test these behaviors meaningfully.

Constraints:
QR/card choices may lead to clearly unfinished views at this stage; never label them complete until Prompt 09. No real payment credentials. Rejecting cash must not create a transaction reference presented as a successful sale. Success/receipt screens will be completed in Prompt 10.

Expected output:
Working method selection and validated cash completion, verified arithmetic and failure behavior, evidence updates, and an explanation of why browser validation alone is insufficient. Stop before Prompt 09.
```

## Prompt 09 - Implement simulated QR and card payments

```text
Context:
Cash validation and shared completion logic are ready. Apply shared rules and F13-F15.

Objectives:
Complete the two other required payment methods with honest simulation behavior.

Requirements:
QR: show the current amount, a clearly identified simulated QR/placeholder, scanning instructions, and a Confirm Payment control. Card: show amount, tap/insert/swipe instruction, Process Payment control, and a short visible processing state before completion. For both, use the shared validated completion logic, amount paid equal to total, and zero change. Preserve correct order/method details and prevent duplicate completion. Include understandable feedback and safe Back behavior. Verify each method, stale/empty order handling, and repeated completion attempts.

Constraints:
No actual QR banking integration or collection/storage of card details. Label simulations clearly. A timer or visual processing animation alone must not bypass server validation. Do not add elaborate payment-provider code.

Expected output:
Verified QR/card flows, consistent recorded amounts and methods, evidence updates, and an explanation of simulation versus real payment processing. Stop before Prompt 10.
```

## Prompt 10 - Implement success, receipt, and clean reset

```text
Context:
All three payment paths can complete transactions. Apply shared rules and F15-F19 plus confirmation/feedback requirements.

Objectives:
Finish the required transaction sequence accurately and isolate consecutive customers.

Requirements:
Success must show confirmation, transaction amount, amount paid, payment method, reference, and View Receipt. The digital receipt must show reference, local date/time, items, quantities, unit prices or subtotals, total, method, amount paid, and change matching the stored completed sale. Use Asia/Singapore display time unless we agree otherwise. Add New Transaction on the receipt; reset cart, active payment details, current receipt/reference, and total, returning to empty selection. Retain historical database sales if that is our storage decision, but prevent the next customer from recovering the previous active receipt through ordinary Back/reload/direct-link behavior. Ensure invalid or incomplete payments cannot open a successful receipt and unrelated sessions cannot read it. Verify two successive sales have different references and receipts.

Constraints:
Printing is optional and excluded from this milestone. Do not render receipt values from a mutable live cart. Do not delete completed-sale history to implement active-state reset. Do not claim the whole exam complete before integration checks and evidence review.

Expected output:
A complete verified transaction flow, cash/QR/card receipt checks, reset/isolation results, evidence updates, and a walkthrough of one sale from selection to new transaction. Stop before Prompt 11.
```

## Prompt 11 - Polish the original interface and feedback

```text
Context:
The complete transaction flow works. Apply shared rules, DESIGN.md, and F02/F20 without changing agreed business behavior.

Objectives:
Make the kiosk feel polished, modern, calm, and easy to use.

Requirements:
Inspect every screen and its empty/error/loading/success states. Improve spacing, typography, hierarchy, product-card presentation, currency alignment, touch targets, contrast, visible focus, responsive layout, and feedback. Check intended tablet/desktop sizes and a narrower fallback, browser zoom, long product names, and larger currency amounts. Respect reduced motion and communicate errors near the relevant control. Use our own styling and modest decoration. Rebuild local Tailwind assets and confirm styles work without external CDN requests. Recheck affected interactions after edits.

Constraints:
No optional feature expansion or imitation of the sample UI. Do not substitute visual polish for correctness. Do not claim browser inspection if it was unavailable; state the remaining visual checks.

Expected output:
A visually reviewed, consistent interface, recorded observations/fixes, and a concise explanation of how the design supports touch use. Stop before Prompt 12.
```

## Prompt 12 - Refactor a real improvement and explain it

```text
Context:
The app works and visual polish is done. Apply shared rules and checklist sections B/D for meaningful AI-assisted refactoring.

Objectives:
Improve an actual maintainability issue while preserving behavior and documenting evidence.

Requirements:
Inspect for genuine duplicated calculations/payment logic, mixed responsibilities, unclear names, or unnecessary complexity. Choose a small justified improvement; record original code and the reason, prompt/response, final change, tradeoffs, and before/after verification. Keep expected behavior unchanged and run the relevant regression checks. Explain the improvement so I can evaluate it myself. Leave a pending field for my own evaluation/adaptation instead of inventing it.

Constraints:
Do not deliberately worsen code or fabricate a refactoring need for the rubric. If no meaningful issue exists, record that honestly and explain the evidence gap. Avoid broad rewrites and implementation-mirroring tests.

Expected output:
A justified refactor when warranted, before/after evidence and verification, or an honest finding that no refactor is justified. Stop before Prompt 13.
```

## Prompt 13 - Run the complete exam acceptance checks

```text
Context:
All planned functionality and polish are present. Apply shared rules and the instructor tests on pages 7-8 summarized in EXAM_PLAN.md.

Objectives:
Verify every required behavior and identify failures before final documentation.

Requirements:
Run all 15 instructor scenarios with our catalog's equivalent expected calculations: startup/touch selection, multiple products, quantities, removal, summary, preserved Back navigation, three methods, insufficient cash, successful/exact cash, confirmation, receipt, QR, card, reset, and distinct references. Include blank/invalid/negative cash, nonnegative quantities, consistent amounts, failed-payment absence of success/receipt, QR/card zero change, and consecutive-customer isolation. Use automated checks for meaningful backend behavior and browser/manual checks for actual interactions and appearance. Record date, actual tested revision or uncommitted state, expected/observed outcomes, and evidence in TEST_RESULTS.md. For failures, capture the real error and use the debugging prompt; rerun relevant checks after repairs. Map F01-F20 and A-F to verified evidence and remaining gaps.

Constraints:
Do not mark unrun checks passed or fabricate screenshots/results. Do not add features to hide failures. Mark unavailable visual/environment checks pending. Keep genuine member/Git/AI gaps distinct from application failures.

Expected output:
An acceptance report, accurate checklist updates, any real fixes with debugging evidence, and clear remaining blockers. Move to Prompt 14 only once functional failures are resolved or explicitly documented.
```

## Prompt 14 - Finish documentation and audit development evidence

```text
Context:
Acceptance checks have been recorded. Apply shared rules and checklist sections A-E.

Objectives:
Make setup reproducible and development evidence reviewable without inventing missing activity.

Requirements:
Complete README with purpose, stack, storage rationale, prerequisites, exact setup/migration/seed/Tailwind/run/test commands, payment simulation notes, workflow, and known limitations. Verify documented commands using an appropriate isolated check that does not destroy working data. Audit AI_LOG.md for generation, genuine debugging, genuine refactoring, critical evaluation, adaptations, and responsible members. Audit MEMBER_REGISTER.md for actual accounts, tasks, branch names, commits, PR source/target, reviews before merge, feedback resolution, and integration commit. Identify absent evidence explicitly. Explain that the professor's each-member requirement remains unmet where real feature work is missing; help list genuine remaining contributions or a question for the professor. Use the Git checkpoint prompt to carry out authorized repository work separately.

Constraints:
Documentation cannot manufacture history, peer review, cloning demonstrations, or human understanding. Do not label the group compliant simply because documents have headings. No deployment or submission. Avoid exposing secrets or personal credentials.

Expected output:
Verified README and truthful evidence records, an A-F audit with remaining items, and a short explanation I can use to understand the architecture. Stop before Prompt 15.
```

## Prompt 15 - Prepare the demonstration and individual explanations

```text
Context:
Our application and documentation are ready for a final readiness review. Apply shared rules and checklist section F.

Objectives:
Prepare an accurate, understandable demonstration and identify anything still needed before the exam.

Requirements:
Create docs/DEMO_GUIDE.md with verified startup steps, a short required-flow demonstration, invalid and insufficient cash, exact payment, QR/card simulations, receipt checks, distinct references, and reset. Include troubleshooting for likely setup issues based on actual project behavior. Prepare questions and explanatory notes about cart state, Decimal calculations, server validation, snapshots, reference generation, simulations, AI decisions/adaptations, and Git workflow. Assign explanations only to actual contributions in MEMBER_REGISTER.md; invite all three members to rehearse their own understanding. Review F01-F20 and A-F and summarize verified readiness, pending human explanations/reviews, and known limitations. Record the actual final integration revision after it exists.

Constraints:
No guarantees of a perfect grade, no invented member answers, and no automated submission/deployment. Pending contributions or reviews stay pending. Do not treat this demonstration guide as evidence that the demonstration has already happened.

Expected output:
DEMO_GUIDE.md, a final honest readiness checklist, and a practical rehearsal sequence I can follow. Stop here; perform only separately requested remaining work.
```

## Reusable prompt A - Debug a real problem when it occurs

Use this between stages when a real error or failed check occurs. Paste the actual error and expected/observed behavior after the prompt when available. Do not invent a bug solely for evidence.

```text
Context:
We are working on the current IT415 kiosk milestone. Apply the shared rules in docs/BUILD_PROMPTS.md, inspect the current files/logs and the actual failure I provide, and read EXAM_PLAN.md. If a traceback or reproduction detail is missing, try relevant non-destructive checks and ask only for information still needed.

Objectives:
Find and fix the actual cause while helping me understand the error.

Requirements:
Capture the real error/reproduction and expected versus observed behavior. Diagnose before editing, explain the likely cause, make a focused fix, and rerun the reproduction plus relevant regression checks. Record the original error, this prompt/response, changed code, responsible member if known, and actual verification in AI_LOG.md and TEST_RESULTS.md. State uncertainty and pending human evaluation honestly.

Constraints:
No unrelated rewrites, invented failures/results, destructive data resets, or completion of later milestones. Protect secrets in logs.

Expected output:
A verified focused fix or an honest unresolved diagnosis, debugging evidence, an explanation I can follow, and the numbered stage we should resume.
```

## Reusable prompt B - Record a milestone in Git and open a review PR

Invoke during development at genuine milestones, not only after the app is finished. This prompt authorizes a scoped commit, push, and review PR for the current milestone, subject to actual repository access. It does not authorize merging. If a PR already exists for the branch, update that PR instead of creating a duplicate.

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

## Reusable prompt C - Merge a genuinely reviewed PR

Use only after real review and feedback resolution. This prompt explicitly authorizes merging the eligible current milestone PR, without overriding repository rules.

```text
Context:
The current kiosk milestone PR is ready for integration. Apply the shared rules in docs/BUILD_PROMPTS.md. I authorize merging this PR after you verify its actual review status and required checks.

Objectives:
Integrate reviewed work and record genuine review/merge evidence.

Requirements:
Identify the current intended PR, source and target branches. Verify genuine review before merge, record the reviewer and feedback resolution, and check the latest revision's relevant checks. Merge only when those requirements and repository rules are satisfied. Record PR URL, actual merge/integration revision, and verification in MEMBER_REGISTER.md and EXAM_PLAN.md. Keep the local work safe and verify integration without discarding changes.

Constraints:
Do not bypass branch protection or treat AI inspection as an absent human peer review. Do not invent approval. If review/checks are missing, leave the PR unmerged, explain the gap, and continue independent work that is safe.

Expected output:
An actual recorded merge and integration check when eligible, or a concrete explanation of why it remains pending. No deployment or submission.
```

## Reusable prompt D - Resume in a later chat

```text
Context:
Continue my IT415 POS kiosk project from its current state. Read docs/BUILD_PROMPTS.md, EXAM_PLAN.md, DESIGN.md, and existing evidence records, plus applicable repository instructions. We use an original modern design and proceed one milestone at a time. Our group has three members; do not infer anyone's contribution.

Objectives:
Recover the actual project state and continue only the next agreed unfinished milestone.

Requirements:
Inspect current files, Git state, completed checks, open issues, decisions, and evidence gaps. State what is verified, what is merely planned, and the next numbered prompt. If the current milestone is clear, perform its scoped work using its five fields and shared rules. If the intended milestone is ambiguous, finish the read-only recovery and ask for that clarification.

Constraints:
Do not rebuild completed work, execute the entire guide, manufacture evidence, or overwrite local changes. Do not auto-commit, push, merge, deploy, or submit.

Expected output:
An accurate recovery summary and one completed, verified milestone when its scope is clear, with updated records and an explanation I can understand.
```

## Reusable prompt E - Start a feature branch before editing

Use before the next feature milestone. This authorizes local branch preparation only, not commits, pushes, PR creation, or implementation of multiple stages.

```text
Context:
We are ready for the next numbered kiosk feature stage. Read docs/BUILD_PROMPTS.md, EXAM_PLAN.md, and MEMBER_REGISTER.md, and inspect the current checkout. I authorize preparing the local feature branch before we edit that feature.

Objectives:
Put the next feature's actual work on an identifiable branch without losing current changes.

Requirements:
Identify the next milestone and actual contributor from confirmed facts. Inspect the current branch and working changes. Reuse the appropriate feature branch if one already exists; otherwise create a descriptive codex/ branch from the correct integration state. Preserve all local files and avoid carrying unrelated work into the feature. If uncommitted setup or another feature must be recorded first, explain the concrete dependency and use only independently authorized actions; do not discard it. Record the real branch and intended task, distinguishing intended assignment from completed contribution. Verify the resulting branch state.

Constraints:
No impersonation, resets, force operations, commits, pushes, PRs, merges, or automatic feature implementation. If the state prevents a safe branch transition, leave files intact and report it.

Expected output:
A safely prepared and documented local feature branch, or a specific unresolved checkout dependency. Identify the next numbered prompt to paste.
```

## Coverage map

| Requirement area | Main prompts |
| --- | --- |
| A: problem, users, inputs/outputs, choices | 01-02; rationale finalized in 14 |
| B: generation/evaluation/adaptation records | All stages from 03; member evaluation must be real |
| B: genuine debugging | Reusable A whenever a real failure occurs |
| B: genuine refactoring | 12 when a meaningful improvement exists |
| C: genuine branches, commits, PRs, review/merge and seven real stages | Reusable E before feature edits; B/C throughout; audit in 14 |
| D: code organization/validation/consistency | 05-10, 12-13 |
| E: README, AI log, member register | 03 onward; audit in 14 |
| F: working demo and individual explanations | 13 and 15; actual human rehearsal remains necessary |
| F01-F06: selection/cart/calculation/touch | 04, 06 |
| F07-F08: summary and preserved Back | 07 |
| F09-F12: methods and cash validation/change | 08 |
| F13-F15: QR/card and amount consistency | 09-10 |
| F16-F19: success/reference/receipt/reset | 10 |
| F02/F20: touch interface and feedback | 04, 06-11 |
| All 15 instructor test scenarios | 13 |

This guide covers the reviewed requirements; it does not prove completion or promise a grade. Only implemented behavior, observed checks, genuine records, and members' actual understanding can establish readiness.
