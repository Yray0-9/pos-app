# IT415 kiosk exam: requirements and working plan

## Latest accepted storage/publication change

Magos explicitly replaced the previous SQLite decision with no database and authorized deletion/public Vercel deployment. Current architecture is the fixed server catalog plus signed-cookie cart and active receipt, described in DATA.md. No permanent history/global payment lock/copy-cookie revocation is claimed. All payment screens remain simulations; QR intentionally uses a demo placeholder as the requirement permits. Earlier SQLite design and verification statements below are retained as historical stages, not current promises.


Prepared: 2026-10-07 (Asia/Singapore).

## Purpose and boundaries

This is the persistent checklist for our step-by-step work. Read and update it when continuing the project. It records assignment requirements; it does not authorize automatic implementation, publication, or submission.

The user wants guidance and understanding at each stage, an original interface, and complete coverage of the exam and photographed checklist. Magos's latest request permits adapting the sample's menu-and-order organization while retaining Common Table's own branding, colors, typography, products and artwork. DESIGN.md section 13 is the current layout direction; earlier behavioral-reference-only statements describe the previous plan.

Historical completion checkpoint: complete database-free simulated kiosk, public at https://common-table-kiosk.vercel.app and locally http://127.0.0.1:8000/. 21 database-free tests pass, including isolated main checkout (1.367s); local/public HTTP/CSRF flows pass. SQLite deleted. Completion e4fa2ba and review-history reconciliation c7cd068 were pushed to cart-review. Normal main merge 0764e0815e1b6f678e1c9c6b2e4a2de2e577931c was pushed and remote SHA verified. Tested runtime is identical on feature/main/public deployment dpl_CaAD2UzZwta8KY6YdfZCnAsYw1Z9. No force/history rewrite or invented review. Current main excludes private/generated files; old history remains. Browser touch/layout/JS evaluation, genuine member contributions/independent review and final instructor process acceptance remain pending. Earlier SQLite/46-test and deployment-deferred entries are historical, not current guarantees.

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

The table states pass conditions. Current implementation/evidence status is in the combined-completion section below; new browser/human/process checks remain pending.

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
3. Setup and workflow: foundation/configuration checks and initial evidence records complete. Authorized setup commit pushed on codex/setup-foundation; [PR #1](https://github.com/Yray0-9/pos-app/pull/1) open into main. Reviewer/merge, instructor/member verification, and clone demonstration pending.
4. Selection and review: implement and verify cart operations, calculations, summary, and preserved Back navigation.
5. Payments: implement and verify cash validation, QR confirmation, and card processing.
6. Completion: implement and verify success, references, receipt, and New Transaction reset.
7. Final preparation: run the full instructor test flow, complete evidence and README, and rehearse individual explanations.

At each implementation milestone: explain the change, implement the agreed scope, verify its pass conditions, record actual evidence, and update this document before proceeding. Do not build every milestone in one turn merely because this plan exists.

## Authorized setup Git checkpoint

User invoked reusable B on 2026-10-07. The existing Git author Yray0-9 was preserved, and authenticated GitHub account Yray0-9 was verified with push access. Setup commit: [a20201aeb262959b4d38f5f80bed78a3b5e8d56f](https://github.com/Yray0-9/pos-app/commit/a20201aeb262959b4d38f5f80bed78a3b5e8d56f). Source branch: codex/setup-foundation; target: main. [PR #1](https://github.com/Yray0-9/pos-app/pull/1) exists and is attached to this chat. It is unmerged and has no reviews at this checkpoint. No reviewer was messaged or assigned; genuine teammate review still needs a confirmed account. MEMBER_REGISTER.md records the actual evidence and remaining individual gaps. Documentation updates recording the resulting links remain part of this same scoped milestone.

## Local UI branch preparation

Reusable E completed on 2026-10-07 at about 12:17 Asia/Singapore. Clean setup branch 717b165 was the base; setup PR #1 was checked and is still open/unmerged. Created local codex/ui-foundation at the same commit and recorded intended Prompt 04 work under Magos, not completed feature authorship. No files were discarded, no identities changed, and no commits/pushes/PRs/merges or UI implementation occurred. Parent setup is an explicit dependency: future UI PR compares against codex/setup-foundation while it remains unmerged; inspect/retarget only through later authorized Git work. Branch records are uncommitted on the UI branch. Next numbered stage: Prompt 04 only.


## Prompt 04 outcome — original interface foundation

Verified locally on 2026-10-07, about 12:20–12:33 Asia/Singapore, against setup HEAD `717b165` plus uncommitted UI changes. Reusable E authorization and current branch were confirmed before application edits. Existing branch-preparation records were preserved. Requester: Magos; implementation: Codex assistance, with human evaluation/explanation pending. No Agbas/Daro work is asserted.

- Added the `kiosk` app and root route/view; `pos_app` retains project-wide configuration. The view renders templates without database/session/cart operations.
- Added original Common Table branding, cream/green/plum styling, static SVG artwork/favicon, system typography, a skip link, progress include, feedback/messages includes, and a full-width menu area above the empty order area. No current transaction step is asserted. Disabled review has an explanatory hint; the only disclosure is a real native HTML interaction.
- Tailwind CSS/CLI 4.3.3, pnpm 11.19.0 and Node 24.19.0 were observed. Pinned dependencies/lockfile, explicit Django-template source detection, CSS theme/configuration, production/watch scripts, and built local CSS exist. No CDN or external font is used. Package caches remain ignored.
- System/dependency checks, root/CSS/favicon HTTP responses, CSS reproducibility, watcher updates, feedback escaping/semantics, active-step template variants, keyboard skip/focus/disclosure, and desktop/tablet/narrow overflow checks passed. See TEST_RESULTS.md and the saved screenshot for exact scope.
- F02/F20 have foundation evidence only; products and the functional transaction flow remain pending. Error/success/loading feedback variants are reusable markup, not demonstrated payment behavior. No full functional checklist item is upgraded solely from this foundation.
- No application models, migrations, catalog seed, cart calculations, payment flows, receipts, reset, login, or inventory were implemented. No Git mutations occurred in this stage. Existing setup PR remains the dependency; UI branch/commit/push/PR review evidence is still to be recorded through reusable B.

Next numbered prompt: 05, catalog and transaction data foundations, after the genuine interface Git checkpoint and next feature branch preparation. The earlier seven broad milestones are a planning outline; numbered BUILD_PROMPTS.md controls the smaller staged implementation requests.


## Prompt 04 visual refinement and Git preference

2026-10-07, approximately 12:39–12:52 Asia/Singapore. Magos described the initial rendered design as old-fashioned and requested a more modern, modest, appealing design before moving on. This authorizes design iteration within the existing UI milestone, not catalog/data/transaction implementation. The revised page has a lowercase wordmark/CT symbol, a dark forest welcome panel with restrained lime details, stronger editorial typography, an original local food SVG, a cooler light canvas, smaller horizontal menu-unavailable card, and a more polished full-width order card. The ordered Choose/Review/Pay/Receipt information and accessible controls remain. The name, catalog proposal, data direction and products-above-order structure are retained. The actual visual revision is pending user feedback; no satisfaction or approval is asserted.

Magos explicitly intends to handle Git actions personally. The assistant should tell them when the genuine milestone is ready to record and guide/check results, rather than running commits/pushes/PR/merge/branch operations under prior authorization. After design acceptance, preserve this interface milestone before moving into Prompt 05 on its prepared feature branch. Instructor/member evidence requirements and actual review gaps still apply; no action or contribution is inferred from the preference alone.


## Authorized UI Git checkpoint outcome

2026-10-07, approximately 12:57–13:00 Asia/Singapore. Reused the pre-established codex/ui-foundation branch; configured author and authenticated account Yray0-9 retained without impersonation. Reviewed 28-file interface/evidence milestone committed as [6ff4a07](https://github.com/Yray0-9/pos-app/commit/6ff4a07cbc410b3436c6f6e2c4ed152fac33977b) and pushed with upstream tracking. [UI PR #2](https://github.com/Yray0-9/pos-app/pull/2) opened from codex/ui-foundation to codex/setup-foundation and was attached to this chat. Parent setup PR #1 remains open/unmerged at 717b165; main remains initial 9e959ad. This base isolates the UI changes. Future integration/base reconciliation needs separate authorization.

At creation the UI review list was empty. A later [Copilot COMMENTED entry](https://github.com/Yray0-9/pos-app/pull/2#pullrequestreview-5437802476) reported quota exhaustion and no inline findings. No substantive feedback to resolve, human approval or CI pass is asserted. A genuine non-author reviewer is required: Agbas/Daro with confirmed account or an instructor-accepted reviewer. No reviewer was assigned or messaged. Interface now exists in real committed history; other members' feature work, individual verification and seven required real stages remain incomplete. A follow-up evidence-only commit records actual links/statuses on this UI branch, not an extra application stage.

## Prompt 04 sample-layout adaptation

2026-10-07, approximately 13:00-13:18 Asia/Singapore. Magos requested a menu/order organization closer to the supplied sample, retaining our own theme and project. DESIGN.md section 13 now supersedes the full-width order layout. Local page has six static illustrated cards beside the desktop empty-order panel, with responsive stacking. Brand, catalog proposal, SQLite/session architecture and transaction requirements are unchanged. This is presentation only: F01-F20 functional pass conditions remain pending, including genuine selection, review, payment, receipt and reset.

Existing reusable E evidence applies to this same UI milestone/branch. Reused codex/ui-foundation at HEAD fa76162 without Git mutation. Revision and evidence are uncommitted and not in PR #2. Other members' actual feature work/review/understanding remain unresolved; no contributions or human approval were invented. Next action is Magos's visual feedback; then a scoped UI Git checkpoint, reusable E and Prompt 05 when requested.

## Reusable E - Prompt 05 checkout prepared

At the next request, the UI workspace/evidence were already committed as 3cad483d1e930c23c0ae7d8f0e34ae451cdadd57, with a clean checkout. Local origin/UI matched; no network refresh or new PR evidence asserted. Magos explicitly authorized local branch preparation and requested advancing. Created codex/catalog-data at that UI SHA to preserve the complete application foundation, then recorded intended Prompt 05 work under Magos. No feature implementation, models, migrations, commits, pushes, PR changes, merges or identity changes.

Integration issue found from actual local trees: main and origin/main now point to 141af0103e8e73630acf76f867bfb5caeed07efe, diverging from UI history. Main tracks .env, node_modules and caches and lacks manage.py, settings and requirements; it is not the prepared integration result. No private values were read into output. Keep this separate from catalog work. Before integration, resolve the tracked private/generated files and missing application history, and assess/replace the secret if it was published. This checkpoint does not authorize history rewriting, cleanup commits, merging or secret changes.

Branch task is pending implementation. Next: paste Prompt 05 from BUILD_PROMPTS.md. Existing design/data decisions apply; personal evaluation, other member implementations, peer review and final acceptance remain unresolved.

## Prompt 05 outcome - persistent data foundation

2026-10-07, approximately 13:44-14:03 Asia/Singapore. Actual branch catalog-data, UI base 3ce83e25975870cc8fbadb42c3267086729117d7. Implemented Product, completed Transaction and TransactionItem with Decimal fields, unique CT UUID references/attempts, method enum, timestamp/context and historical line snapshots. Added initial migration and seed_catalog; applied 19 migrations including standard Django dependencies. Six agreed products created; second seed preserved IDs/values. Local sale/item counts zero; 14 tests passed using separate in-memory SQLite. No cart/payment/receipt/reset endpoints or UI binding were added. F01-F20 functional acceptance stays pending; these are underlying data/storage checks.

Shared pricing/completion responsibilities and every field are explained in DATA.md. Exact calculations will use Python Decimal, with server catalog prices; future completion must validate a nonempty current reviewed order, context/attempt and all line/header totals, then atomically persist and handle repeat requests. Schema uniqueness/rollback tests alone do not prove idempotent payment HTTP handling or consecutive-customer isolation.

User-requested UI evidence commit: 3ce83e2 on codex/ui-foundation, configured author Yray0-9; seven prior documentation files only. Not pushed by this stage. Replaced unused local codex/catalog-data (no unique commits) with catalog-data from that updated UI base. No reset, force operation, impersonation, merge, PR change, deployment or reviewer contact. Current data/evidence uncommitted; no fabricated extra development stage. Main/security and genuine member/review gaps remain. Proposed workflow groups 06-07 on cart-review and 08-09 on payments to limit branch proliferation. Next numbered prompt: 06 after the scoped Git checkpoint and branch preparation when requested.

## Reusable E for Prompt 06 - prior milestone must be recorded first

Current catalog-data checkout still contains uncommitted Prompt 05 Product/Transaction/TransactionItem models, initial applied migration, seed command, data tests and documentation. No appropriate cart-review branch exists. A new branch from current HEAD would bring the prior milestone's uncommitted work along, obscuring the catalog commit/feature responsibility; using main/UI instead would omit the required data foundation. Nothing was discarded, stashed, reset, committed or switched.

This is a checkout dependency under the user's E constraints, not a reason to fabricate history or repeat tests. Record the catalog milestone first through explicitly invoked reusable B or actual user Git actions. Then run E again to prepare cart-review from the resulting complete catalog state, and paste Prompt 06. Pending cart implementation and genuine member/review evidence remain distinct from already passing data tests.

## Prompt 06 outcome - selection and current order

2026-10-07, approximately 14:22-14:37 Asia/Singapore. Existing authorized cart-review branch confirmed before feature editing. Seven branch-preparation documents already changed at entry and were preserved. No Git mutations, migration changes, payment flow, review screen, receipt or reset.

| Requirement | Local evidence | Remaining boundary |
| --- | --- | --- |
| F01 selectable catalog | Six available SQLite products with real names/prices; click/tap adds, repeated selection combines quantities | Instructor/human demonstration pending |
| F02 touch interaction | Cards and quantity/remove controls at least 48 CSS pixels, Review 56; keyboard Enter and visible focus; responsive checks | Physical touchscreen, assistive-technology assessment and future-screen navigation pending |
| F03 quantity adjustment | Add/increase/decrease; strict session integer validation, range 1-99; decrease one removes; rejected requests preserve order | Direct arbitrary quantity editing is not offered |
| F04 removal | Explicit Remove deletes line; recalculated order and feedback | Locally verified, not instructor sign-off |
| F05 exact amounts | Shared Decimal calculator fetches current DB prices; PHP 279.50/364.50/240.00 scenario verified | Future review/payment must reuse calculator and validate reviewed facts |
| F06 current order | Name, unit price, quantity, subtotal, total and unit count shown | Order-review requirements F07-F08 remain pending |
| F20 feedback | Adds, decreases, removals, limits, stale entries and network recovery have feedback; loading and busy controls implemented | Payment errors/processing/success remain pending; live screen-reader behavior not verified |

The cart survives reload. Empty order is PHP 0.00 and cannot advance. Review remains disabled even for a nonempty order because that feature is next; this is not claimed as completed review. Server trusts IDs/quantities in its session and current product data, never browser price/total fields. Separate browser sessions are isolated in tests; New Transaction isolation is not yet implemented. Damaged/stale session entries are disclosed and only repaired on an explicit POST, with clear feedback.

All 24 data/cart tests passed. Root/CSS/JS loading, browser arithmetic/removal/reload, focus, sizes and overflow checked at 1280x900, 768x1024 and 360x800. Tablet/narrow order follows menu using normal page scroll. Live database remains six products, zero completed sales/items. See TEST_RESULTS.md and evidence/cart-desktop.jpg.

A real browser bug (hidden action field shadowed form.action) was found and fixed using the form action attribute; full browser flow then passed. It is honest debugging evidence within this milestone, not an invented separate commit/stage. Git recording, genuine peer review, Magos's personal verification/explanation and other member contributions remain pending. Next: scoped B checkpoint, then Prompt 07 on cart-review.

## Combined local completion — current functional evidence

2026-10-07. User explicitly requested execution so they can test the app. Existing prepared cart-review at f901b32 was clean and reused without Git mutation. Prior local review files were absent; review was rebuilt from the shared calculator. Required completion code and evidence remain uncommitted. Preview runs on 8001, leaving the pre-existing 8000 server intact.

| Requirement | Implemented / checked evidence | Remaining check |
| --- | --- | --- |
| F01 | Six available products, visible names/prices; selection tests and live HTTP adds | Personal touch selection |
| F02 | Existing >=48px controls; new >=56px buttons/keypad, labels, focus styles, responsive panels | New visual/touch/keyboard/screen-reader/contrast/zoom checks |
| F03-F06 | Trusted Decimal quantities/subtotals/total; increase/decrease/remove/zero and invalid inputs | Personal interaction rehearsal |
| F07-F08 | Exact current summary and read-only Back; 279.50/364.50/240.00 arithmetic and repeated navigation | Browser layout and Back interaction |
| F09 | Three real method links to working forms | Personal choice interaction |
| F10-F12 | Cash amount due, keypad, Pay Now; invalid cash rejected with no sale; exact/overpay/change verified | Browser keypad interaction |
| F13 | Labeled QR placeholder/instructions/Confirm Payment; snapshot total, paid=total and zero change verified | Personal QR flow |
| F14 | Card instructions, Process Payment, 1200ms visible JS processing; correct backend completion checked | Visible delay requires actual browser test |
| F15-F18 | Shared atomic completion, unique attempt/reference, stable snapshots, success and full receipt, timezone/method/paid/change agree | Personal screen comparison |
| F19 | Signed POST reset clears active state and rotates context/session; history retained; old/other-session receipt access blocked | Browser Back/reload/cache interaction |
| F20 | Escaped add/error/processing/success feedback with roles; stale/empty/invalid order guards tested | New loading/error/focus screen behavior |

46 tests pass, including atomic partial-write rollback and actual simultaneous same-attempt completion. Live HTTP/CSRF covers all three methods, invalid cash, duplicate submit, owned receipt, reset and distinct references; three acceptance sales retained in local history. Existing migrations are applied; no new schema/dependency changes. Fresh temporary-database migration/seed/reseed/check passes. Built local CSS and all JS syntax checks pass. Browser control unavailable: no new screenshot, card-delay interaction or visual/touch/accessibility pass claimed. See TEST_RESULTS.md and DEMO_GUIDE.md.

| Checklist section | Present evidence | Remaining gap |
| --- | --- | --- |
| A requirements | Original problem/users/inputs/outputs and F01-F20 plan retained | Instructor verification |
| B AI assistance | Actual combined request, generated architecture, adaptations, tests and limits in AI_LOG | Human critical evaluation/adaptation/explanation; full transcript reference; no separate refactor fabricated |
| C Git/member workflow | Existing feature history retained; current branch/base observed | Current completion commit/push/PR/review/merge, seven real stage audit, member contributions and final integration |
| D code quality | Shared calculator/completion, isolated snapshots and guarded transitions; 46 regressions | Human code review and real issues found in rehearsal |
| E docs | Setup, state/storage/simulation limits, tests and demo guide updated | User/instructor document review and final integration SHA |
| F demonstration | Backend/HTTP flow verified, personal rehearsal guide supplied | Physical browser/touch demo and all three members' independent explanations |

No work is attributed to unavailable members. Functional implementation does not establish individual feature credit, genuine peer review or seven committed development stages. Public deployment is deferred. Next: Magos's local rehearsal, real fixes if needed, then separately authorized Git checkpoint/review; no next numbered prompt is required merely to run the app.
