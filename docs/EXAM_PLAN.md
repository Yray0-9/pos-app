# IT415 kiosk exam: requirements and working plan

Prepared: 2026-10-07 (Asia/Singapore).

## Purpose and boundaries

This is the persistent checklist for our step-by-step work. Read and update it when continuing the project. It records assignment requirements; it does not authorize automatic implementation, publication, or submission.

The user wants guidance and understanding at each stage, an original interface, and complete coverage of the exam and photographed checklist. The sample UI is a reference for behavior only. Do not reproduce its branding, colors, or layout as our design.

Current stage: Prompt 03 foundation and initial evidence records completed on 2026-10-07. Next: authorized setup Git checkpoint, then feature branch preparation and Prompt 04 UI foundation. Current user: M3 - Magos; deadline: 2026-10-07 at 21:00 Asia/Singapore. Individual accounts and separately issued rubric/submission rules remain pending. No kiosk features exist. Checkboxes indicate verified completion, not intention; setup HTTP success is not a complete application pass.

Sources reviewed:
- `C:/Users/Romul/Downloads/IT415_Practical_Exam.pdf`: all 8 pages.
- `C:/Users/Romul/Downloads/IT415 - Sample UI.pdf`: all 10 pages.
- Attached checklist image: sections A-F. Its bottom member-number line is partly cropped; do not infer group size from it.
- `C:/Users/Romul/Downloads/IT415 Acceptance Checklist.pdf`: all 4 pages extracted and visually inspected during Prompt 03.

The user confirmed a three-member group and currently expects to do the implementation personally with AI assistance. The other two members' actual contributions are not established. Record the work honestly; personal implementation cannot by itself satisfy each-member feature/contribution, review, and explanation requirements. Seek genuine participation or an instructor-approved arrangement, and keep unmet items visible.

Confirmed user-supplied details: Instructor Reban Cliff A. Fajardo, MIT; intended repository https://github.com/Yray0-9/pos-app; members M1 - Agbas, M2 - Daro, M3 - Magos. The current user identified themselves as M3 - Magos. Deadline: 2026-10-07 at 21:00 Asia/Singapore, interpreted from "later 9pm" in the current client date/timezone. Repository access and individual account ownership have not been verified; do not assume that the repository owner identifies a particular member.

The instructor may have separately issued AI/GitHub requirements. Those remain to be confirmed, along with individual member accounts. Prioritize required features and evidence within the supplied deadline; do not skip real verification or invent completion. Do not infer rubric weights or submission requirements that were not supplied.

Prepared copy-and-paste prompts are in `docs/BUILD_PROMPTS.md`. They are future instructions to invoke one stage at a time, not authorization to execute the entire guide now.

### New Acceptance Checklist requirements (Prompt 03 review)

Page 1 contains 26 functional checks, covered by F01-F20 and the final acceptance run. Page 2 requires one shared group repository unless otherwise specified; personal repositories are not required. Record group number/name, section, project title, repository namespace, integration branch, final demonstrated SHA, instructor access, local clone demonstration, and branch/network evidence URL or screenshot reference. Group number/section/evaluation date remain pending.

Pages 2-3 require actual member identities, feature branch names, implemented tasks, commit SHA/count, PR URL/number, reviewer, and accurate open/unmerged/merged status. A branch deleted after merge remains verifiable through PR and commit history; do not automatically mark it missing.

Page 4 explicitly requires at least seven real development stages in commit history covering setup, interface, core functionality, validation, genuine bug fix, genuine refactoring, and documentation. Commits must reflect real work; do not create artificial stages or authored identities. The per-member matrix checks identity, feature work, authored commits, pushes, PR ownership/review/merge explanation, AI generation/debugging/refactoring, evaluations/adaptations, and individual code demonstration. The form uses P/F/N/A when verified/assigned; our working register uses Pending until evidence exists, not an automatic pass or exemption.

The new PDF provides a contribution/process evidence format but does not require Word as the documentation format. It references a separately issued grading rubric that has not been supplied. PDF pass/fail and instructor fields have not been filled or altered; MEMBER_REGISTER.md and TEST_RESULTS.md support later completion.

## Starting state observed

- Django project package: `pos_app`; entry point: `manage.py`.
- Default Django applications and admin URL only; no custom kiosk application yet.
- SQLite was configured in the starting settings; the SQLite/session storage direction was subsequently accepted at Prompt 02. Kiosk records are not implemented.
- README contains only the project name.
- Local branch is `main`, tracking `origin/main`; history shows an initial commit.
- `manage.py` and `pos_app/` are untracked at inspection time.
- These observations do not verify server startup, GitHub access, dependencies, or completed functionality.

The above list is the initial state. Prompt 03 subsequently verified Python 3.14.4 / Django 6.1.2, installed python-dotenv 1.2.4, added dependency/ignore/environment setup files and evidence records, extended README, and verified a temporary default welcome page HTTP 200. Changes remain uncommitted on main; only README was previously tracked. The sanitized origin matches the supplied repository. No migrations were applied; temporary startup created an ignored empty db.sqlite3 with no tables. Server stopped after verification. See TEST_RESULTS.md for observed checks and limits.

## A. Requirements analysis

- [x] Document the problem: manual order encoding and total computation at a campus outlet.
- [x] Identify users: customers using a self-service touchscreen; evaluators running the demonstration.
- [x] Identify inputs: selected products, quantity actions, removal actions, payment method, cash amount, simulated confirmation, navigation, and reset.
- [x] Identify outputs: current order, item subtotals, total, validation feedback, processing/success feedback, reference number, and digital receipt.
- [x] Explain technology and data-storage choices and their limitations below. User accepted the design/storage direction after Prompt 02; implementation verification remains pending.

Required sequence:

Select items -> Review order -> Choose payment -> Process payment -> Payment successful -> View receipt -> New transaction.

Screens may be combined if this sequence and its functions remain clear.

### Prompt 01: minimum complete scope

The baseline is one local web kiosk for a campus food/merchandise outlet. It replaces manual encoding and computation with touch selection, a reviewable order, simulated payment, and a digital receipt. No cashier account is needed for the required customer flow. Evaluators and student developers are secondary users of the demonstration and documentation, not additional customer roles requiring screens.

Deliver all F01-F20 behaviors with six or more independently selected catalog items, prices displayed in pesos, an original modern design, and the documented development process in A-F. No inventory, discounts, customer accounts, reports, printing, or live financial integration is in the first release. A product catalog and completed-sale storage are recommended internal implementation choices, not extra professor-mandated features.

| Step | Customer input | Required visible output / state | Requirement mapping |
| --- | --- | --- | --- |
| 1. Select items | Tap product; increase/decrease; remove | Six or more named/priced products; cart items, quantities, subtotals, total; feedback | F01-F06, F20 |
| 2. Review order | Back or Continue | Exact current order and total; Back preserves editable selections | F07-F08, F20 |
| 3. Choose method | Cash, QR, or Credit/Debit Card | Three large choices and the current amount due | F09, F15 |
| 4. Process payment | Cash amount/Pay Now; QR confirmation; card Process Payment | Cash errors or correct change; QR instructions/placeholder; card processing state | F10-F15, F20 |
| 5. Payment successful | View Receipt | Success, amount, amount paid, payment method, distinct reference | F16-F17, F20 |
| 6. View receipt | Read receipt; New Transaction | Date, reference, actual purchased items, quantities, prices/subtotals, total, method, paid amount, change | F15, F18 |
| 7. Start new transaction | New Transaction | Empty selection/cart; total zero; active payment/receipt details cleared | F19-F20 |

F02 (touch-friendly controls) applies across every step. Failed payment must not advance to steps 5-6. QR/card simulations use paid amount = order total and zero change. Quantity cannot become negative. Correct server calculations and preserved state support agreement between all screens.

### Prompt 01: proposed architecture and reasons

The following is the recommended baseline to finalize in Prompt 02, not a claim that these components are implemented.

| Component | Proposed responsibility | Reason / limitation |
| --- | --- | --- |
| Existing Django project + one kiosk app | Configuration in the project; kiosk URLs, views, forms, and business logic in the app | Builds on the scaffold; keeps scope understandable. App not created yet. |
| Django templates | Render customer pages from server-provided data | A separate frontend framework/API is unnecessary for this flow; reusable base templates keep screens consistent. |
| Locally built Tailwind CSS | Original palette, spacing, responsive layout, and touch controls | Gives consistent styling; requires a documented CSS build but no CDN access during evaluation. |
| Modest JavaScript | Touch cash keypad, feedback, and visible simulated card processing | Improves interaction; it must not be the authority for prices, validity, or successful sales. |
| SQLite + Django models | Product catalog, completed sales, and item snapshots | Simple local file storage for this exam. Proposed scope is a local kiosk, not a production payment or multi-store system. |
| Django session | Active customer's cart and current transaction/receipt access | Preserves ordinary Back navigation; reset must clear the previous customer's active state. |
| Shared calculation/completion logic | Decimal totals, payment validation, atomic sale creation, unique references | Avoids inconsistent logic across three methods; repeated payment submissions must not create extra sales. |

Proposed records: Product (name, decimal price, selectable status); Transaction (unique reference, date/time, method, total, amount paid, change); TransactionItem (product/name/price snapshot, quantity, subtotal). Do not accept posted browser prices as trusted amounts. Storing a receipt snapshot prevents later catalog edits or cart changes from rewriting a completed sale.

Use the session for active state and database records for completed transactions. New Transaction clears the active cart/payment/receipt access; it does not delete historical records. A transaction-history screen remains out of scope. Real gateway integrations, banking credentials, and card-number collection are excluded.

Official references checked for the proposed approach (not dependency-version verification):
- Django templates: https://docs.djangoproject.com/en/6.1/topics/templates/
- Django sessions: https://docs.djangoproject.com/en/6.1/topics/http/sessions/
- Django decimal model fields: https://docs.djangoproject.com/en/6.1/ref/models/fields/#decimalfield
- Tailwind local CLI build: https://tailwindcss.com/docs/installation/tailwind-cli

### Prompt 01: development-checklist coverage

| Checklist section | Planned evidence / action | Current status |
| --- | --- | --- |
| A. Requirements analysis | Problem/users/inputs/outputs above, F01-F20 mapping, stack/storage rationale | Planning documented; design/storage direction accepted after Prompt 02 |
| B. AI use | Actual generation prompt/response records, member evaluations/adaptations; genuine debugging and refactoring with verification | Prompt guide prepared; formal log and human evaluations pending |
| C. Git/GitHub | Real setup/feature history, member branches, pushed commits, PRs, review before merge, feedback resolution, final integration revision | All development workflow evidence pending; initial scaffold history is not complete evidence |
| D. Code quality | Clear responsibilities, reused calculations, validated inputs, consistent order/payment/receipt behavior | Pending implementation and checks |
| E. Documentation | README, AI log, member register; linked test and review evidence | Planning files exist; full records pending |
| F. Demonstration / understanding | All 15 instructor scenarios plus validation checks; each member explains their actual code, AI choices, and Git work | Pending implementation, verification, and real rehearsal |

Do not confuse a written plan with fulfilled functionality, peer review, or human understanding. Screenshots may support records; actual commits and PR review/merge history are still needed.

### Prompt 01: proposed genuine member work

The user has stated that they currently expect to do implementation personally with AI assistance. No implemented work by the other two members has been established. The following is an optional genuine redistribution, not an assignment already accepted or completed.

| Person | Small feature they could actually implement | Supporting work | What they need to explain |
| --- | --- | --- | --- |
| Current user: M3 - Magos | Foundation, catalog/cart, review flow, and cash validation/shared completion | Integration and evidence coordination; review teammates' actual changes | State, decimal calculations, validation, chosen architecture, and AI adaptations |
| Other member A (identity pending) | QR and card views/templates using the established completion interface; card processing feedback | Verify QR/card paid=total and change=0; review a teammate's PR | Simulation state, method handling, tests, and their code/AI changes |
| Other member B (identity pending) | Success/receipt templates and active-state New Transaction reset using the established sale data | Verify snapshots and consecutive transactions; review a teammate's PR | Receipt source, reset behavior, reference checks, and their code/AI changes |

Each implemented task should be developed by its actual contributor on a feature branch established before editing, with meaningful commits, a pushed PR, real review before merge, and documented feedback resolution. Proposed branch labels may describe work (for example `codex/payment-simulations`); names alone do not establish authorship. Use the actual person's configured identity, not a substitute identity. These future Git steps are not authorized by this planning prompt.

Review/testing/documentation contributions are useful, but do not by themselves establish a member's implemented feature on a feature branch where the checklist requires one. Reading code after someone else writes it also does not change authorship. The assistant can explain, review, and assist; it does not become a third student member or prove student understanding.

If the other members cannot implement any real task, keep their implementation items pending and clarify the acceptable arrangement with the instructor. Do not fill their contribution records with work performed by the current user or AI. No one will be contacted automatically.

### Prompt 01: unresolved facts and readiness

- Exam deadline supplied: 2026-10-07 at 21:00 Asia/Singapore.
- Member names supplied: M1 - Agbas; M2 - Daro; M3 - Magos. Current user: Magos. Individual GitHub accounts remain pending.
- Separate AI/GitHub rules and Word/PDF/submission-format requirements: not supplied.
- Other members' availability and accepted responsibilities: not established.
- Shared repository access, cloning demonstration, and real review participation: not verified.
- Original name/catalog/layout and SQLite/session storage direction: accepted after Prompt 02. Detailed state policies and runtime behavior still require implementation verification.

These gaps do not block independent design planning. They do prevent claims that the group workflow or all-member assessment requirements have been satisfied. Prompt 01 created the documented baseline; the subsequent Prompt 02 proposal follows below. No runtime checks, dependency installation, migrations, application edits, Git mutations, or server changes were performed for Prompt 01.

### Prompt 02: design and data proposal

Prepared `docs/DESIGN.md` with a proposed Common Table identity, cream/green/plum palette, six original catalog items, responsive product grid above a full-width order list, and all required customer/feedback states. Proposed control sizes are at least 48 CSS pixels; actual rendered accessibility remains to be verified.

Data recommendation: SQLite Product/Transaction/TransactionItem records and a database-backed session cart. Money is computed with Python Decimal; server calculations are authoritative. Completed item snapshots preserve receipts independently of later cart/catalog changes. Database-unique references distinguish sales; unique payment-attempt UUIDs and atomic writes prevent duplicate completion. Active customer context and receipt guards isolate consecutive customers. Reset clears active state and receipt access, not historical sale rows. These correctness policies are design recommendations, not additional quoted exam requirements.

| Choice | Current status |
| --- | --- |
| Django foundation, original modern calm design, Tailwind permitted, gradual work | User-confirmed direction |
| Common Table name, specific palette/layout, six-product catalog | Direction explicitly accepted 2026-10-07 |
| SQLite/session split | Direction explicitly accepted 2026-10-07 |
| Decimal policy, snapshots, unique reference/attempt, reset guards | Supporting design specifications; implementation verification pending |
| Agbas/Daro/Magos names and instructor/repository details | User-supplied facts; no contribution or access verification implied |
| Current user and deadline | Magos (M3); 2026-10-07 at 21:00 Asia/Singapore, user-supplied |
| Member task allocation, individual usernames, separate rules | Pending |

Prompt 02 verification: documented mappings reviewed; proposed solid-color text contrast calculated. No screen, model, migration, dependency installation, server change, or Git mutation performed. Runtime behavior and visual rendering are not verified. The user subsequently answered "Accept the proposed direction" to the design/storage review question. Prompt 03 is next when requested; keep later feature implementation in its own stages.

## Functional acceptance checklist

All entries below are pending implementation and verification.

| ID | Requirement | Pass condition |
| --- | --- | --- |
| F01 | Six or more selectable products | Each shows name and price; tapping/clicking adds it without typing its name. |
| F02 | Touch-friendly interaction | Large controls, readable text, spacing, clear labels, minimal typing, simple Back/Continue navigation. |
| F03 | Quantity adjustment | Increase and decrease work; quantity never becomes negative; invalid quantities receive meaningful feedback. |
| F04 | Item removal | User can remove a selected product; cart and total update. |
| F05 | Subtotals and total | Subtotal = unit price x quantity; total = sum of subtotals; every relevant action updates these values. |
| F06 | Visible current order | Product name, unit price, quantity, subtotal, and transaction total are available. |
| F07 | Order summary | All selected products, quantities, prices, subtotals, and total match item selection. |
| F08 | Back navigation | Returning to item selection preserves products and quantities and allows editing. |
| F09 | Payment choices | Large Cash, QR Payment, and Credit/Debit Card options are available. |
| F10 | Cash payment | Show total, amount-paid input, and Pay Now; compute change = paid - total. |
| F11 | Cash validation | Reject blank, invalid, negative, and insufficient amounts; stay on payment; no successful transaction or receipt. |
| F12 | Exact/overpayment | Exact payment succeeds with zero change; overpayment succeeds with correct change. |
| F13 | Simulated QR payment | Show amount, clearly identified QR code/placeholder, scanning instructions, and confirmation control; confirmation completes payment. |
| F14 | Simulated card payment | Show amount, tap/insert/swipe instruction, Process Payment control, and short processing state before success. |
| F15 | Payment consistency | Order, payment, confirmation, and receipt totals agree; simulated QR/card paid amount equals total and change is zero. |
| F16 | Payment success | Show success, transaction amount, amount paid, payment method, transaction/reference number, and View Receipt control. |
| F17 | Distinct references | Complete two different transactions; their references differ. |
| F18 | Digital receipt | Show transaction reference, date, products, quantities, unit prices or subtotals, total, method, amount paid, and change, matching the completed sale. |
| F19 | New Transaction | From receipt, clear active cart, payment details, previous receipt, and total; return to item selection with no previous customer details. |
| F20 | Meaningful feedback | Clearly communicate additions, invalid quantities, payment errors, processing, and completion. |

Implementation choices to discuss later: block checkout for an empty order, compute trusted totals on the server, use decimal arithmetic for money, and prevent repeated payment submission from creating duplicate sales. These support correctness; they are not additional quoted rubric requirements.

## Required scope versus optional scope

Initial scope: every F01-F20 behavior plus the development evidence below.

Optional: categories, product images, search, inventory, discounts, login, reports, receipt printing, full-screen mode, product management, transaction-history interface, database persistence, and actual QR generation. Real payment gateway/card integration is not required.

If inventory is added, selection must respect available stock and rejected payments must not reduce stock. A screen-based receipt is sufficient; printing is optional. Product names and prices in the exam are examples, not mandatory catalog values.

Accepted planning direction: Django with server-rendered templates, locally built Tailwind CSS for the original modern design, modest JavaScript, SQLite product/completed-sale records, and a session cart. Detailed implementation remains for the later scoped stages; no separate frontend framework is planned.

## B. AI use and AI-assisted development

- [ ] Generation prompts state context, requirements, constraints, and expected behavior.
- [ ] Debugging evidence includes the actual error, prompt/response, applied fix, and verification.
- [ ] Refactoring evidence includes original code, improvement, and behavior verification.
- [ ] Record relevant prompts/responses with the responsible member.
- [ ] Members evaluate correctness, suitability, and limitations of AI output.
- [ ] Members meaningfully adapt generated solutions and explain their changes.

Record evidence as the work happens. Do not invent errors, reviews, member work, or retrospective results to satisfy the checklist.

Suggested log entry format:

```text
Date/time:
Member:
Requirement/task:
AI tool:
Prompt and response record/link:
Actual error or original code (when relevant):
Evaluation of correctness, suitability, and limitations:
Changes the member made and why:
Verification action, expected result, and observed result:
Files/commit/PR links:
```

AI_LOG.md now records actual planning/setup prompts and labeled response excerpts/summaries under M3 - Magos. Full response transcript export/share reference and Magos's own evaluation remain pending. Planning/tool corrections do not establish genuine kiosk application debugging or refactoring evidence.

## C. Git/GitHub workflow

- [ ] Shared repository is accessible to the required members; cloning and local Git use are demonstrated.
- [ ] At least seven real stages represented in actual history: setup, UI, core logic, validation, genuine bug fix, refactoring, and documentation (Acceptance Checklist page 4).
- [ ] Meaningful commits make contributions identifiable.
- [ ] Record each member's feature branch and implemented task.
- [ ] Push branch commits; feature PRs identify source and target branches.
- [ ] Review before merging; record reviewer and resolution of feedback.
- [ ] Merge completed PRs; record the final integration commit used for demonstration.
- [ ] Record branch/network evidence, repository namespace, group number/section, instructor access, local clone demonstration, and each member's verification matrix in MEMBER_REGISTER.md.

Use genuine feature development and review; do not manufacture history. The existing scaffold still needs to be recorded properly when implementation setup begins. Group size and any separate instructor workflow rules must guide task allocation.

## D. Code quality

- [ ] Organize readable code with clear names and logical structure.
- [ ] Reuse repeated logic sensibly and separate responsibilities.
- [ ] Validate inputs and show helpful errors.
- [ ] Keep calculation and payment logic consistent across order, payment, and receipt.

## E. Documentation

- [x] README explains current setup, actual dependencies, scaffold run steps, accepted technology/storage direction, member status, and limitations. Future feature/Tailwind/migration/test commands must be added and verified at their stages.
- [ ] AI development log covers generation, debugging, refactoring, evaluation, and edits.
- [ ] Member register links verified accounts, branches, tasks, commits, PRs, and review/merge evidence. Initial register/matrix exists; missing evidence remains pending.

Suggested member register columns: Member | GitHub account | Task | Branch | Commits | PR | Review performed | Feedback resolved | Merge commit.

## F. Demonstration and individual understanding

- [ ] Application starts and runs without critical errors during evaluation.
- [ ] Selection, quantity controls, removal, summary, and Back navigation work.
- [ ] Cash, QR, and card flows work; invalid/insufficient cash is rejected.
- [ ] Receipt values are correct; transaction references differ; New Transaction resets the active customer flow.
- [ ] Every member can explain their contribution, AI decisions, code, and Git workflow.

## Instructor test baseline

These calculations use the exam's sample catalog only. Substitute equivalent calculations if our original catalog differs.

| Test | Expected result |
| --- | --- |
| Coffee 45 x 2 + Sandwich 50 x 1 + Soft Drink 35 x 1 | Subtotals 90, 50, 35; total 175. |
| Increase coffee quantity from 2 to 3 | Coffee subtotal 135; total 220. |
| Decrease coffee back to 2 | Total returns to 175; no negative quantities. |
| Remove soft drink | Total becomes 140. |
| Review and go Back | Values agree; selected products and quantities remain editable. |
| Cash 100 for total 140 | Reject with clear error; no success/receipt. |
| Cash 200 for total 140 | Success; change 60. |
| Exact cash 140 for total 140 | Success; change 0. |
| Blank/invalid/negative cash | Reject and remain on payment. |
| QR confirmation / card processing | Successful simulation with correct method, paid = total, change 0. |
| View receipt | Values and reference match the completed transaction. |
| New Transaction | Empty cart, total 0, previous active payment/receipt cleared. |
| Complete another transaction | Reference differs from the earlier transaction. |

The PDF provides 15 instructor tests across pages 7-8. Verification must cover all of them, including startup and touch selection, not just the arithmetic examples.

## Step-by-step milestones

1. Requirements and scope: planning documented; current user/deadline recorded; individual accounts and separate rules still pending.
2. Design and data decisions: original layout/catalog/SQLite-session direction accepted; responsibility assignments and implementation verification pending. Planning stage completed.
3. Setup and workflow: foundation/configuration checks and initial evidence records complete. No Git mutations performed; setup checkpoint, instructor/member access, and clone demonstration pending.
4. Selection and review: implement and verify cart operations, calculations, summary, and preserved Back navigation.
5. Payments: implement and verify cash validation, QR confirmation, and card processing.
6. Completion: implement and verify success, references, receipt, and New Transaction reset.
7. Final preparation: run the full instructor test flow, complete evidence and README, and rehearse individual explanations.

At each implementation milestone: explain the change, implement the agreed scope, verify its pass conditions, record actual evidence, and update this document before proceeding. Do not build every milestone in one turn merely because this plan exists.
