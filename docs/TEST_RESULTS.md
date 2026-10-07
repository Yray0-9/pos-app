# Verification results

Prompt 03 foundation, 2026-10-07, approximately 11:49-11:55 Asia/Singapore. Checks below were run by Codex for Magos's requested setup milestone. Human demonstration remains separate.

## Tested state

- Windows PowerShell; existing `venv`, Python 3.14.4, Django 6.1.2.
- Local branch `main`, tracking `origin/main`.
- Existing HEAD: `9e959add21248068edc3230e7774f0cb65d365d3`.
- Setup changes and Django scaffold are **uncommitted**; this SHA does not contain the tested working files. Repeat relevant checks after changes/integration and record the actual revision.
- Installed requirements: asgiref 3.12.1, Django 6.1.2, python-dotenv 1.2.4, sqlparse 0.6.0, tzdata 2026.5. pip 26.0.1 was observed as tooling.

## Observed checks

| ID | Action | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| S01 | Existing environment: Python/Django version, pip list | Identify actual versions | Python 3.14.4; Django 6.1.2 | Verified |
| S02 | Initial `manage.py check` | Configuration loads | System check identified no issues (0 silenced) | Verified before changes |
| S03 | Initial `pip check` | No dependency conflicts | No broken requirements found | Verified before changes |
| S04 | Install python-dotenv | Install into existing project venv | Initial sandbox socket denial; authorized retry installed 1.2.4 | Installed; not an app bug |
| S05 | `scripts/init_env.py` | Create private configuration without displaying secret | Created local .env; no values were displayed | Verified |
| S06 | `manage.py check` after configuration changes | Settings load correctly | System check identified no issues (0 silenced) | Verified |
| S07 | `pip check` after install | Dependencies consistent | No broken requirements found | Verified |
| S08 | `pip install --no-index -r requirements.txt` | Pins match available installed dependencies | All five packages already satisfied | Verified in existing venv; not a fresh online install |
| S09 | Temporary `runserver 127.0.0.1:8000 --noreload`; GET `/` | Running scaffold responds | HTTP 200; Django default welcome page identified | Verified scaffold HTTP only |
| S10 | Stop the owned verification server | Temporary process ends | Ctrl+C ended exec session | Stopped; no persistent server left by this check |
| S11 | Run initializer again and compare .env bytes | Existing local file preserved | True; bytes unchanged | Verified |
| S12 | Subprocess with temporary nonsecret environment overrides | Environment overrides .env; DEBUG=False and host parsed; timezone correct | Assertions passed for override, False, localhost, Asia/Singapore | Verified; actual key not displayed |
| S13 | Subprocess with empty DJANGO_SECRET_KEY | Clear setup failure | Nonzero exit and expected Set DJANGO_SECRET_KEY message | Verified expected failure |
| S14 | Inspect settings without exposing original/current key | No hard-coded development secret | Source check passed; settings read environment | Verified |
| S15 | `git check-ignore` on private/generated paths | .env, venv, cache, DB, node_modules ignored | All checked paths ignored | Verified |
| S16 | `git check-ignore` on shareable/source paths | Template, requirements, evidence, future migration/CSS paths not excluded | None excluded | Verified ignore rules; future files not claimed to exist |
| S17 | Inspect local repository state and sanitized origin | Identify real branch/history/tracking | main -> origin/main; initial commit; origin matches supplied repo | Read-only verification; remote access not verified |
| S18 | Inspect SQLite state after startup | No migrations applied | Local db.sqlite3 exists with 0 bytes and no tables | Confirmed uninitialized; ignored file |
| S19 | New Acceptance Checklist PDF | Review all relevant pages | Extracted and visually inspected all 4 pages | Requirements reconciled in plan/register/guide |

A first one-line verification helper failed due to shell quoting (`SyntaxError: unterminated string literal`). It was replaced with a standalone scratch verification script; S11-S16 then passed. This is an assistant tooling correction, not a fabricated application debugging test or qualifying kiosk bug fix. The scratch script and PDF renders are outside the repository in this chat's visualization workspace.

## Limitations and pending checks

- No fresh clone/new-venv installation demonstration was performed; dependency satisfaction was verified in the existing venv.
- No migrations were run. The local database has no application/auth/session tables; database-dependent admin functionality is not ready.
- No browser visual check or kiosk interaction was performed. The HTTP success is Django's default welcome page, not a POS acceptance pass.
- No kiosk models, products, cart, payment, receipt, reset, Tailwind build, or functional tests exist yet.
- No Git staging, commits, branches, pushes, PRs, reviews, or merges occurred in this stage.
- No instructor access or individual member verification is asserted.

## Later acceptance verification

All 26 functional rows from page 1 of the Acceptance Checklist and all 15 scenario tests from pages 7-8 of the Practical Exam remain pending for the actual kiosk. Map them to F01-F20 in EXAM_PLAN.md and record expected/observed results when implemented. Include blank/invalid/negative/insufficient/exact cash, QR/card zero change, distinct references, preserved Back navigation, and previous-customer reset/isolation.

For each future check: record date/time, responsible member/verifier, requirement ID, exact tested revision or uncommitted state, action, expected result, actual result, evidence link, and failure/fix where applicable. Do not mark pending checks passed.

## Authorized Git checkpoint (2026-10-07, about 12:06 Asia/Singapore)

- Django system check and pip dependency check rerun before committing: both passed.
- Reviewed staged diff: 17 scoped foundation/scaffold/planning/evidence files; `git diff --cached --check` passed.
- Secret exclusion scan: local .env secret absent from all selected contents; no original `django-insecure-` setting committed. Private files remained ignored.
- Remote main verified as the initial SHA before setup push; no existing setup PR matched the branch.
- Setup code commit: `a20201aeb262959b4d38f5f80bed78a3b5e8d56f`; configured author Yray0-9. The setup code matches the verified Prompt 03 state; later checkpoint changes are documentation-only.
- Branch push succeeded and upstream was configured. [PR #1](https://github.com/Yray0-9/pos-app/pull/1) opened from codex/setup-foundation to main and was attached to this chat.
- API state: open, merged=false, author Yray0-9, no reviews at this checkpoint. No review feedback was fabricated/resolved and no merge/deployment performed.
- Instructor access, other members' accounts/work, peer review, fresh clone demonstration, and the functional acceptance matrix remain pending.
- After evidence commit c7860f7 was pushed, remote PR head matched that commit and the working tree was clean; changes since a20201a were documentation-only. GitHub check runs/statuses were empty, so no CI pass is asserted. The later Copilot COMMENTED entry reported quota exhaustion and had no inline findings; it is not a successful code review or human approval. This actual review attempt was inspected and recorded; no application changes were required from it.


## Prompt 04 — UI foundation verification

Date: 2026-10-07, approximately 12:20–12:33 Asia/Singapore. Verifier: Codex tools/browser, requester Magos; this is not a human member/instructor test record. State: local codex/ui-foundation at HEAD `717b165c852ad2c771fbc506ffb3578529a75b46` plus uncommitted foundation/doc changes. Prior Prompt 03 limitations above describe that earlier stage.

| ID | Action / expected result | Actual observed result |
| --- | --- | --- |
| U01 | Confirm reusable E before feature editing | Current codex/ui-foundation and prior explicit E record confirmed; branch head equals setup dependency; four existing documentation edits preserved |
| U02 | Inspect tooling and lock dependencies | Node 24.19.0; pnpm 11.19.0; Tailwind/CLI 4.3.3 pinned in package.json and pnpm-lock.yaml |
| U03 | Locked install after cache download | `install --frozen-lockfile --offline` succeeded with CI=true; 33 packages reused, no download. No fresh clone/new-machine install claimed |
| U04 | Production CSS build | `run build:css` succeeded, Tailwind v4.3.3. Repeated final builds produced identical SHA256 `f7c78186d96fe4b7fb9fa30360d1e7ed0b870fbf8f52bf3313f93b2207654197` |
| U05 | Watch mode detects Django-template changes | Interactive `run watch:css` remained active; temporary template with decoration-double triggered rebuild and generated utility. Probe removed, watcher stopped and final minified CSS rebuilt |
| U06 | Django configuration and Python dependencies | `manage.py check`: no issues (0 silenced); `python -m pip check`: no broken requirements |
| U07 | Root and local static delivery | Root HTTP 200, Common Table title/local CSS link; stylesheet HTTP 200 text/css and bytes identical to built file; SVG favicon HTTP 200; `findstatic` resolved kiosk CSS |
| U08 | Reusable feedback and progress rendering | Scratch Django rendering checked error alert, other status roles, loading aria-busy, escaped script input; each progress step 1–4 emitted exactly one aria-current. Not payment outcome tests |
| U09 | Desktop preview at 1280×900 | Inspected branding/hero/menu/order/disclosure; document clientWidth=scrollWidth=1265 (scrollbar excluded), no horizontal overflow |
| U10 | Tablet preview at 768×1024 | Inspected spacing/legibility; clientWidth=scrollWidth=753, no horizontal overflow |
| U11 | Narrow preview at 360×800 | Header/text wrapped; clientWidth=scrollWidth=345, no horizontal overflow |
| U12 | Keyboard skip/focus/disclosure | Tab showed Skip to content with plum outline; Enter focused main-content; disclosure Enter opened instructions and had visible focus outline. Browser viewport override restored |
| U13 | Typography and controls | Computed body font 18px. Skip control 48px; brand link about 56px; disabled Review and disclosure 56px high |
| U14 | Palette contrast calculation | ink/canvas 12.00:1; muted/white 5.75:1; muted/soft-green 4.94:1; leaf/white 8.16:1; plum/white 7.97:1; error/error-surface 6.18:1. Border/decorative and disabled-control colors are not claimed as normal text contrast tests |
| U15 | Save visual evidence | docs/evidence/ui-foundation-desktop.jpg saved from final full-page browser view; preview retained at localhost |
| U16 | Final shareable-file/checkout verification | Final root/CSS/hash passed; private secret absent from all 33 shareable tracked/new files; .env, venv, node_modules and .pnpm-store ignored; git diff --check passed; still codex/ui-foundation with uncommitted changes; probe removed |

Observed issues and resolution: initial registry access was denied by sandbox EACCES; the authorized dependency operation completed with permitted access. pnpm reported an undecided Parcel watcher build script; the workspace now explicitly skips it, and its platform prebuilt watcher passed U05. Noninteractive sandbox commands attempted module-store recreation and were interrupted; permitted local install/build completed. These are development-tool setup limitations, not fabricated kiosk bug-fix stages. Initial CSS HTTP 404 occurred because runserver --noreload started before the new static directory existed; restarting discovered the directory and U07/browser CSS then passed. Build-before-run guidance was added. The temporary probe was removed.

Pending: physical touch interaction, actual screen-reader test, 200% zoom, OS reduced-motion preference toggle, other browsers/operating systems, fresh clone/new-machine setup and all catalog/cart/payment/receipt/reset scenarios. Reduced-motion support was inspected in source, not claimed as OS-tested. No models or migrations were added/run. Interface Git evidence and actual teammate evaluation/review remain pending. The root view does not require initialized database tables.


## Prompt 04 modern visual revision

2026-10-07, approximately 12:39–12:52 Asia/Singapore. Verifier: Codex tools/browser; requester Magos. Same local UI branch/setup HEAD plus uncommitted design revision. Earlier U01–U16 describe the first foundation, not this revised CSS hash.

- Tailwind 4.3.3 local production build passed. Revised CSS SHA256: `27e3b533fff98da349fe60268eff2fd470ba2ed2c45ad1c751b7c658287c8c33`.
- Root HTTP 200 contains revised title and original illustration reference. CSS, illustration and favicon returned HTTP 200 with bytes matching local files. Both SVGs parsed as valid XML. Decorative hero image loaded successfully in the browser.
- `manage.py check` and `git diff --check` passed. Progress rendering still produces exactly one active step for each supplied step 1–4; the foundation itself has no active transaction.
- Browser inspected at 1280×900, 768×1024 and 360×800. Document clientWidth equaled scrollWidth: 1265, 753 and 345 respectively. No horizontal overflow. Artwork moves below text on narrow screens; order controls and disclosure wrap.
- At narrow width, control heights: skip 48px, brand 50px, disabled Review 56px, disclosure 80px. Tab exposed the skip link with visible plum outline; Enter focused main-content. Native summary Enter opened the explanation and had a visible outline; it was closed again for the screenshot.
- Contrast calculations: ink/new-canvas 12.27:1, muted/new-canvas 5.39:1, white/forest 11.70:1, lime/forest 9.21:1. Previously verified error/white/soft-green token combinations are retained.
- Saved revised full-page screenshot: docs/evidence/ui-foundation-modern-desktop.jpg. Earlier screenshot retained. Temporary browser viewport override restored; updated preview retained at localhost.

Observed preview issue: --noreload kept the earlier HTML in the template loader cache while serving the revised CSS. Restarting the local development server loaded the revised templates; README now mentions this behavior. Two browser keyboard attempts targeted a child span/assumed button role and failed; targeting the native summary succeeded. These are preview/tool targeting observations, not fabricated application bug-fix stages. The initial patch was rejected because it attempted delete/add of the same home.html in one patch; no partial file edits occurred from that rejected patch, and the files were then updated normally.

Still untested: physical touchscreen, screen-reader operation, zoom/reduced-motion preference toggles and future transaction screens. No functional POS acceptance pass is claimed. Revised design acceptance is pending Magos. No commits, pushes, PR changes, branches or merges were performed in this revision.


## UI Git checkpoint — pre-commit review

2026-10-07, Asia/Singapore; local codex/ui-foundation at setup HEAD 717b165 plus reviewed UI/evidence changes. Magos explicitly authorized this checkpoint after the visual revision. Checks performed by Codex are not independent peer review.

- Rerun `manage.py check`: no issues (0 silenced); `python -m pip check`: no broken requirements.
- Rerun `pnpm run build:css`: Tailwind 4.3.3 succeeded; output matches the recorded revised SHA256 27e3b533fff98da349fe60268eff2fd470ba2ed2c45ad1c751b7c658287c8c33.
- Root response checked through Django test client: HTTP 200, revised heading/art reference, all stylesheet/favicon/illustration URLs local and files present, only order button genuinely disabled. Feedback error/status roles, loading aria-busy and escaped script content passed.
- Reviewed route/config/template/CSS/build/evidence diff and untracked file inventory. Files belong to the original UI milestone and its evidence; no unrelated user edits identified. Private secret absent from shareable files; ignored local env/venv/database/package caches preserved.
- Confirmed origin fetch/push match Yray0-9/pos-app without embedded credentials. Existing authenticated account Yray0-9 has push permission. Remote setup SHA matches local parent 717b165; main still initial 9e959ad. No remote UI branch or matching UI PR existed before this checkpoint.
- Setup PR #1 verified open/unmerged. Its Copilot COMMENTED entry still reports quota exhaustion; inline findings empty, no substantive review feedback to resolve. No peer-review pass asserted.
- Prior desktop/tablet/narrow/focus checks and screenshots retained; no new app changes justified repeating all browser checks. Physical touch/screen-reader/zoom and full POS scenarios remain pending.


## UI checkpoint — actual Git/PR evidence

- Staged whitespace/scope/private-secret checks passed for 28 UI/evidence files. Local .env, venv, database and caches excluded/preserved.
- Created implementation commit `6ff4a07cbc410b3436c6f6e2c4ed152fac33977b` with configured author Yray0-9. Clean working tree observed immediately after commit; UI push with origin tracking succeeded.
- [PR #2](https://github.com/Yray0-9/pos-app/pull/2) created/attached: open, merged=false, author Yray0-9, source codex/ui-foundation, target codex/setup-foundation, initial head exactly the implementation SHA. No check runs/statuses returned; no CI pass asserted.
- Empty reviews at creation; later inspection found [Copilot COMMENTED quota entry](https://github.com/Yray0-9/pos-app/pull/2#pullrequestreview-5437802476), no inline findings. Genuine human review/feedback resolution pending.
- Main/setup parent verified before push; no force push, merge or deployment. Evidence follow-up changes docs only. A documentation-recording helper first failed to parse an f-string before any file writes; corrected helper recorded actual returned links. This is not an application bug-fix stage. Final branch/remote verification follows the evidence push.

## Prompt 04 menu-and-order workspace revision

2026-10-07, approximately 13:00-13:18 Asia/Singapore. Verifier: Codex tools/browser; requester Magos. Tested state: codex/ui-foundation at HEAD fa76162e758e72da445f729ce0d5e99d0faa8d71 plus uncommitted workspace/evidence changes, not PR #2's committed UI. No independent member verification asserted.

- Tailwind 4.3.3 production build succeeded. Built CSS SHA256: 5345f2764755584dcbc9b641a4ba322f7faf9df71fad4059d7aebfa50e514f9e.
- Django manage.py check: no issues (0 silenced). Root via Django test client: HTTP 200; six product preview buttons and Review disabled; six SVG use references resolve to unique inline symbol IDs; document IDs unique; stylesheet/favicon references local. No database/migration work required.
- Browser displayed local CSS and all six original illustrations. Desktop 1280x900: three product columns beside order panel; document clientWidth=scrollWidth=1265. Compact desktop 1024x768: two product columns beside panel, widths=1009. Tablet 768x1024: two product columns with order below, widths=753. Narrow 360x800: one column with order below, widths=345. No horizontal overflow observed. Page requires vertical scrolling to view all content.
- At narrow width, skip control 48px, Review 56px, disclosure 56px. Desktop product preview buttons approximately 321.6px high. Decorative plus marks are not separate working controls.
- Tab focused Skip to content with a solid plum outline (computed 2.4px); Enter focused main-content. Native summary Enter opened the future-flow explanation with a visible focus outline, then closed again. Disabled product/payment controls cannot initiate a transaction.
- Saved and visually inspected docs/evidence/ui-foundation-workspace-desktop.jpg. Previous screenshots retained as historical evidence. Browser viewport override restored; local preview retained.
- Final git diff --check passed after evidence edits. Browser readback confirmed the local built stylesheet was loaded (37 top-level CSS rules) and system typography applied. No branch/commit/push/PR/merge mutations during this revision.

Browser recovery observation: the previous turn's tab was no longer available. Its empty tab inventory was verified and a new localhost preview was opened. No application defect or bug-fix stage is claimed. Local development server was restarted to refresh cached templates under --noreload. These are preview operations, not exam transaction tests.

Pending: Magos's visual acceptance, physical touchscreen, screen reader, 200% zoom, OS reduced-motion toggle, other browsers/OS, fresh clone and all functional POS scenarios. Static card names/prices and zero total are fixtures; no trusted-money/cart acceptance pass is claimed. Reusing existing palette checks does not establish full accessibility compliance.

## Reusable E - catalog branch checks

2026-10-07, approximately 13:36-13:42 Asia/Singapore; verifier Codex tools, requester Magos. Branch preparation only; no application checks rerun because no application code changed.

- Initial git status --porcelain=v1 was empty. UI HEAD and local origin/UI were both 3cad483d1e930c23c0ae7d8f0e34ae451cdadd57. Existing commit inspection showed the complete 14-file workspace revision, including the product/art includes and screenshot.
- Local branch inventory contained main, setup and UI only; no existing catalog branch to reuse. Configured author name remained Yray0-9; no identity mutation.
- main and local origin/main both 141af0103e8e73630acf76f867bfb5caeed07efe; ancestry comparison main...UI was 1/6 unique commits. Filename-only tree inspection showed tracked .env/generated artifacts and absent prepared sources on main. Secret values were not displayed. Current UI .env/db.sqlite3 remained ignored/untracked.
- Authorized git switch -c codex/catalog-data from UI SHA succeeded. Resulting branch/HEAD checked; immediately clean; git diff against the UI base returned no paths. Local files preserved, no unrelated edits transferred. Branch has no upstream.
- Final branch/status/scope/whitespace checks performed after documentation edits; only evidence/current-status documentation should differ from the UI base. No catalog/model/seed/migration/runtime changes, commits, pushes, PR updates or merges.

No fresh remote server, CI, reviewer or instructor verification asserted. Existing UI tests remain tests of the UI milestone. Prompt 05 verification is pending.

## Prompt 05 and authorized UI evidence commit

2026-10-07, approximately 13:44-14:03 Asia/Singapore. Verifier Codex tools; requester Magos. Final tested state: catalog-data at HEAD 3ce83e25975870cc8fbadb42c3267086729117d7 plus uncommitted data/evidence files. Not a human teammate/instructor test record.

| Check | Actual result |
| --- | --- |
| Initial checkout/setup | Seven evidence edits only; no .env or database initially. First showmigrations failed due to missing DJANGO_SECRET_KEY. Existing init_env.py created ignored private .env with no values printed; retry showed standard migrations unapplied |
| UI commit requested by user | Switched to UI preserving edits; selected exactly seven documentation files; staged secret/scope/whitespace scan passed. Commit 3ce83e2 succeeded with configured author Yray0-9. No push, PR or merge; UI ahead of local origin by one |
| Simple task branch | Created catalog-data from new UI commit; removed unused codex/catalog-data after confirming zero unique commits. Exact SHA/branch verified; local .env preserved; no upstream |
| Data generation/check | New kiosk 0001_initial generated for three models; manage.py check passed |
| First test run | 14 tests ran; required-context case reached NOT NULL IntegrityError rather than ValidationError and caused cascading broken-transaction errors. Other data cases passed. Missing noneditable/server-managed values needed explicit model validation |
| Applied fix/retest | Transaction.clean checks required attempt/context/reference/timestamp explicitly. Extended null/empty checks; final 14 tests passed in separate in-memory SQLite, including unique IDs, Decimal roundtrip/arithmetic, method/cash consistency, invalid money/quantities, snapshot retention, seed preservation, DB constraints and atomic rollback |
| Local migration | Inspected database: empty zero-byte file created by setup inspection, no existing data. Migration plan inspected; 19 migrations applied, including kiosk 0001 and standard dependencies. Nothing deleted or rewritten |
| Local seed/reseed | First command 6 created/0 preserved; second 0 created/6 preserved. IDs unchanged; each stored product passed full_clean and prices were Decimal with agreed two-decimal values |
| Runtime state | Local Transaction/TransactionItem counts both 0. Test sales were isolated to the test database, not demonstration receipts |
| Configuration/migration consistency | manage.py check passed; makemigrations --check --dry-run reported No changes detected; migration executor found no outstanding migrations |
| Existing root | Django client root HTTP 200; presentation remains static/unavailable; no template/CSS/URL/view changes in this stage |
| Final source scope | Final whitespace/private-file/status review performed after evidence updates. Environment, database and generated caches remain excluded from feature files; historical main private-file issue remains separate |

The initial test failure and its real fix belong to this data milestone; they are not counted as a separate fabricated bug-fix stage. No browser styling checks rerun because no rendered code changed. No UI cart/payment, idempotent endpoint, receipt authorization/reset, browser-back, real peer review or all-member acceptance pass asserted. No fresh remote/PR/CI inspection this stage.

## Reusable E for Prompt 06 - checkout inspection only

2026-10-07, approximately 14:03-14:06 Asia/Singapore. Verifier Codex tools; requester Magos. Actual branch catalog-data at 3ce83e25975870cc8fbadb42c3267086729117d7, no upstream. Existing local branches: main, codex/setup-foundation, codex/ui-foundation, catalog-data; no cart-review. UI remains one commit ahead of its locally recorded origin ref.

Initial inventory: seven modified documentation files, new DATA.md and seven Python model/seed/migration/test package files. No catalog implementation commit since the prior turn. Whitespace inspection passed. No remote/PR state refresh and no application tests rerun; prior 14 tests remain results for Prompt 05.

Branch transition was not performed: uncommitted catalog prerequisite needs its own scoped checkpoint, while current user constraints forbid committing it. No stash, resets, removals, Git mutations, migrations or runtime changes. Only five evidence/plan documents changed in this inspection; app/source, README, private environment and local database hashes were checked against the captured baseline after editing. Final branch/HEAD and whitespace/status were verified. No Prompt 06 pass claimed.

## Combined B/E catalog pre-commit review

2026-10-07, approximately 14:10-14:16 Asia/Singapore. Verifier Codex; requester Magos. Before catalog commit: catalog-data at UI evidence SHA 3ce83e2 plus reviewed milestone/evidence changes.

- Reran 14 tests: pass in separate test SQLite. manage.py check and pip check passed; makemigrations --check --dry-run found no changes. No new implementation changes required.
- Local database: six products passed full_clean; completed sales/items zero; migration executor has no pending migrations. Existing root response HTTP 200. Prior seed/visual tests retained; no additional browser/transaction-flow pass claimed.
- Verified origin fetch/push exactly matches intended GitHub repo with no embedded credentials, configured name Yray0-9. Secret absent from shareable files; .env, database and ignored checkpoint helper excluded.
- Fresh authenticated API confirmed Yray0-9 push access, public repo, main at 141af01, UI remote 3cad483, no catalog/cart-review refs or existing catalog PR. Parent PRs #1/#2 open/unmerged; bot quota messages remain non-substantive review.
- Published UI evidence parent 3ce83e2; ordinary push succeeded without force. Private main history unchanged. Privately compared key values: current development key differs from tracked main key; no values printed.
- Catalog staged scope/whitespace/secret review and actual commit/PR results are recorded after their operations. Next stage remains conditional on completing B; no cart code or reviewer messages.

## Catalog B - actual commit/push/PR checks

- Staged 15 selected files; whitespace/scope/private-secret checks passed. Commit a02288bca6d1fda50cfea7191066b25cf47e46e2 created with configured author Yray0-9; clean checkout observed after commit. No application changes during checkpoint.
- Ordinary UI parent push 3cad483..3ce83e2 succeeded. Catalog push created origin/catalog-data/upstream; local/remote-tracking heads matched implementation SHA.
- PR #3 created/attached, open/unmerged, author Yray0-9, head catalog-data at implementation SHA, base codex/ui-foundation at 3ce83e2. Fresh API status found Copilot COMMENTED quota message/no inline findings; checks/statuses empty. No CI/reviewer approval claimed.
- Reviewed diff against UI parent covers this milestone/evidence only. No main change, force push, merge, deployment or reviewer contact. Current private key differs from publicly tracked main key; no values printed. Original main history issue remains unresolved.
- Follow-up docs record actual evidence before E. App checks are the already passing 14 tests/configuration/dependency/migration checks; no browser or payment acceptance added.

## E after catalog B - verified local branch

- Catalog evidence commit 796b5da355b90d55bdddf74429e1998588095738 created/pushed; eight changed files relative to implementation a02288b are documentation only. Clean checkout and local origin/catalog-data equality verified. GitHub PR #3 head matched evidence SHA, open/unmerged, expected UI base; quota-only review, no inline findings/checks/statuses.
- No cart-review branch existed locally or remotely during inspection. Authorized creation from exact committed catalog SHA succeeded. Result: cart-review at 796b5da355b90d55bdddf74429e1998588095738, initial git status empty, git diff catalog-data empty, no upstream. No unrelated changes transferred.
- E then records intended task/actual branch in docs only. Final status/HEAD/whitespace/source-diff checks performed after those records. No application code, models, templates, database, credentials or runtime changed during E; no tests rerun because B's verified application code remains identical.
- No commits/pushes/PRs/merges after E began. Next feature implementation pending Prompt 06. Existing 14 passing tests remain data checks, not functional cart/payment acceptance or human review.

## Prompt 06 - selection/cart verification

Date 2026-10-07, approximately 14:22-14:37 Asia/Singapore. Verifier Codex; requester Magos. Actual local revision: cart-review at 796b5da plus uncommitted feature/evidence changes; no cart commit/CI/human approval. Tests are in kiosk/test_cart.py; prior 14 data tests preserved.

- manage.py test kiosk: 24/24 pass (14 previous data, 10 cart scenarios), separate in-memory SQLite, 0.850s first run. Expected/observed: six available named/priced cards; empty zero/no advance; repeated add combines lines; rice x2 + wrap + lemonade = 279.50; increase rice = 364.50; decrease = 279.50; remove lemonade = 240.00; quantity-one decrease deletes; final empty zero; no completed sale/items.
- Invalid canonical IDs, non-ASCII IDs, absent/unavailable products, unknown actions and absent-line adjustments: friendly error, original state unchanged. Quantity 99 rejects growth; lower quantities recover. Browser price/total/subtotal/quantity inputs never override server amounts/steps.
- Session tests: reload keeps order; distinct Client sessions isolated; context UUID preserved/revision advances; stale review/payment reserved keys cleared by valid edits; unrelated session data retained. No New Transaction/reset verification implied.
- Corrupted negative/zero/100/fractional/bool/string/null quantities and damaged namespace/cart: invalid entries disclosed/excluded; GET leaves saved content untouched; explicit refresh repairs. Removed/unavailable products warn; current DB price changes affect active total. Total storage cap rejects growth and permits reductions.
- /cart/ GET and / POST return 405. Enforced-CSRF missing token returns 403 with no mutation; valid native POST follows redirect and renders escaped product/feedback. Responses include no-store; empty catalog has useful message. Native fallback tested using Django Client, not a browser with JavaScript disabled.
- manage.py check: no issues. makemigrations --check --dry-run: no changes. pip check: no broken requirements. Tailwind 4.3.3 local minified build: pass; no new dependencies. Initial sandbox package-cache/registry access failed; canceled and rebuilt with authorized cache access, reusing 33 packages and downloading zero. No approval review rejection.
- Browser initially found POST /[object HTMLInputElement] 404: hidden input name action shadowed form.action in JS. Fixed URL lookup to getAttribute('action'); reloaded JS, then verified full add/increase/decrease/remove/zero/re-add flow and persisted 279.50 order. Server test success alone did not establish JS success. One exact feedback locator mismatch was corrected to inspect rendered DOM and wait for removed lines; no additional app bug inferred.
- Browser: root/CSS/JS load, available real controls, badge/line count, amounts and reload persistence passed. Keyboard Enter increased rice; focused increment button retained plum outline. Removal restored product-card focus. 1280x900, 768x1024 and 360x800: no horizontal overflow; every workspace button >=48x48 CSS pixels (Review >=56px high). Tablet/narrow order follows menu with normal page scroll. Final console error list empty. Physical touch/screen-reader/full accessibility and artificial network-throttle testing pending; loading code exists but no slow-network visual pass claimed.
- Screenshot evidence/cart-desktop.jpg saved from browser full page and visually inspected. Screenshot order rice x2/wrap/lemonade, 4 units, 279.50. Later browser reload observed rice x3/wrap/lemonade x2, 6 units, 404.00; the shared live order had changed after capture and was preserved without attributing the interaction to a member. Live DB inspected: six products, zero completed transactions/items. No DB deletion, migrations, public admin, payment, receipt or reset changes. Existing runserver stopped/restarted to load feature; current localhost server left running.

F01/F03-F06 locally verified; applicable F02/F20 selection behavior covered only. F07/F08 remain pending. The disabled review control is explicit because Prompt 07 has not been implemented; empty-cart checkout remains a required endpoint guard when introduced. Git checkpoint and human/member/instructor evidence pending.

Final recheck: all 24 tests passed again in 0.924s; Django configuration, dependency/migration drift, node --check cart.js and git diff --check passed. Local branch/HEAD unchanged (cart-review/796b5da); feature screenshot/code are not ignored, temporary documentation helper is ignored. Final browser reload preserved the later 404.00 order and Review remained disabled.

## Cart B checkpoint - precommit review

2026-10-07 Asia/Singapore. cart-review base 796b5da plus reviewed Prompt 06/E evidence. All 24 tests pass in 0.872s; Django configuration/pip checks pass; migration drift absent. Existing Node executable --check cart.js passes; bare node PATH lookup initially failed. Live database six products, completed sales/items zero. Prior browser/CSS evidence remains from Prompt 06; no new visual or payment acceptance claimed.

Reviewed 21 changed/new files, including code, built local CSS, ten cart tests, screenshot and eight docs; removed obsolete disabled fixture template. Whitespace check passes. Origin fetch/push exactly verified; private current secret absent from shareable changed/new files; env/database/cache/tmp remain excluded. Actual author Romulo Magos preserved; authenticated Yray0-9 has push access. GitHub parent heads/review/check state inspected; source cart-review -> target catalog-data pending publication. No commits/pushes/reviews asserted before returned success.

## Combined local completion — final verification

2026-10-07, Asia/Singapore. Requester Magos; checks run by Codex. Tested new uncommitted working files on clean-entry cart-review at f901b32 (the base contains selection, not the new completion). No Git/account/publication changes. Preview started on 127.0.0.1:8001 at 19:43:34, leaving the existing 8000 process intact.

| Verification | Actual result | Status |
| --- | --- | --- |
| Entry/config/data | Existing private environment preserved without output; Django check no issues; all 19 existing migrations applied; seed zero created/six preserved | Pass |
| Automated regression suite | 46 tests in 3.312s: 14 data + 10 cart + 21 checkout + 1 concurrent completion | Pass |
| Summary/Back/edit | Current prices/quantities/subtotals match; 279.50 order -> rice increase 364.50 -> decrease/remove 240.00; repeated GET keeps cart | Pass |
| Cash validation | Empty/text/whitespace/NaN/Infinity/negative/zero/insufficient/too many decimals/exponent/grouped/over-limit values rejected with no sale/receipt; exact 279.50 change 0; cash300 change20.50 | Pass |
| QR/card consistency | Method choices/forms, clear simulation/instructions; total=paid and change0; valid completion/success/receipt | Backend/HTTP pass; browser processing delay unrun |
| Stale/invalid guards | Missing/forged/cross-session/wrong-method tokens, edits, live price/name/availability/deletion changes, malformed metadata, oversized and empty cart cannot complete | Pass |
| Duplicate/atomic completion | Repeated original token creates one sale and preserves original paid amount; two loaded sessions agree; actual parallel same-attempt workers followed by safe explicit retries yield one complete sale; injected second-line write failure rolls back header/lines | Pass; injected failure is a test, not a claimed real application bug |
| Snapshot/receipt | Names/prices/subtotals survive product edits/deletion; correct method/paid/change/timezone/reference; two customers get distinct references/context and own items | Pass |
| Reset/ownership | Active receipt/success blocked for other/reset sessions, old cookie/reference/payment/reset tokens; reset rotates key/context and preserves unrelated session data/history; paid cart cannot be edited until reset | Pass |
| CSRF/methods | Continue/completion/reset reject GET; enforced-CSRF client rejects missing tokens with403 | Pass |
| Live HTTP on8001 | Isolated cookie jar with real CSRF: review/Back/edit/stale confirmation, cash errors/correct change, QR/card, duplicate retry, stored receipts, cross-session denial, reset/old-token denial/distinct refs; CSS/JS HTTP200 | Pass; 3 test sales retained, initial0 -> final3; no user browser cart touched |
| Fresh database setup | Separate new temporary SQLite file: migrate, seed/reseed, six products, zero sales, configuration check | Pass; working data/environment preserved; not a fresh clone/package-install demonstration |
| Build/dependency/schema | Tailwind4.3.3 minified build201ms; Node syntax check of cart/payment/navigation; pip check clean; makemigrations --check --dry-run no changes | Pass |
| Diff | git diff --check checked directly via subprocess: exit0; unchanged branch/base | Pass |
| Final scope/privacy | 28 modified/new milestone files; private development key absent from those files; environment/database/node_modules/temp tools/local plan ignored; local plan untracked; branch cart-review and HEAD f901b32 unchanged | Pass; no Git/account/publication mutation |
| Browser availability | CUA inventory empty; opening iab returned Browser not available: iab | Unrun: new layout/focus/touch/keypad/card-delay/screen-reader/Back-cache checks and screenshot |

The first suite had44 tests and passed; added malformed-metadata/oversize and actual concurrency regressions, final46 pass. No real runtime application failure was observed in this combined build. A PowerShell check group returned1 while configuration/dependency outputs were clean; direct git diff --check confirmed0, so that grouped command exit was not logged as an app failure. Existing environment, packages and database were retained; no dependency upgrade/migration rewrite or cleanup of history.

### Required scenario coverage and manual boundary

The following is our catalog-equivalent rehearsal mapping from EXAM_PLAN's instructor baseline, not invented instructor sign-off or exact professor test numbering:

| Scenario | Equivalent example / observed backend result | Personal browser check |
| --- | --- | --- |
| Startup and selection | Root200; six named/priced products; configuration clean | Pending: actual touch selection |
| Multiple products | Rice85 x2 + Wrap70 + Lemonade39.50 =279.50 | Pending |
| Increase | Rice x3 =>364.50 | Pending |
| Decrease | Return279.50; zero removes line | Pending |
| Remove | Remove lemonade =>240.00 | Pending |
| Summary | Exact current names/unit prices/quantities/subtotals/total | Pending |
| Back | Preserves editable selections; fresh totals after edits | Pending |
| Three methods | Cash/QR/Card routes work | Pending |
| Insufficient cash | 100 for279.50:400 and no sale | Pending |
| Overpayment | 300 for279.50:change20.50 | Pending |
| Exact payment | 279.50:change0 | Pending |
| Success/receipt | Stored amounts/method/date/reference/items match | Pending |
| QR | Confirm records total paid, zero change | Pending |
| Card | Backend records total paid, zero change; JS specifies1200ms processing | Pending: visible processing |
| Reset and next reference | Empty active state/0total; history preserved; references/context differ | Pending: browser Back/cache behavior |

Full exam/process acceptance remains pending personal demonstration, real review/member contributions/explanations, committed development history/refactoring audit and final integration. See DEMO_GUIDE.md. No browser pass is inferred from Node syntax or HTTP checks. Existing selection screenshots remain historical.

## Current database-free and public deployment verification (2026-10-07)

Supersedes earlier SQLite/46-test/8001 results for the current build; those results are
historical. User explicitly requested removing the database and publishing on Vercel.

| Check | Actual result |
| --- | --- |
| Database deletion | Verified root db.sqlite3 removed (three previous test sales); file absent after live flows |
| Current automated suite | 21 SimpleTestCase tests in 1.400s; no database queries permitted; all pass |
| Flow/cash/arithmetic | 279.50 baseline; edits364.50/240.00; invalid cash rejected; exact/excess cash and QR/Card consistent |
| Receipt/reset | Correct snapshots, aware timestamp, method/paid/change/reference; current-cookie serial retry immutable; reset/cross-customer/stale-token guards pass |
| Explicit storage limitations | Copied-cookie replay and conflicting amounts from separate old cookies remain possible; stable attempt reference verified; no global ledger claim |
| Cookie size | Six lines with quantity99 each fit4096-byte header limit |
| Real local HTTP/CSRF | Port8000 full flow passes with isolated cookies; CSS and all JS HTTP200 |
| Real public HTTPS/CSRF | common-table-kiosk.vercel.app full flow passes without Vercel authentication; all methods/receipts/reset/assets checked |
| Config/dependencies/static | Django check clean; pip check clean; six static files collected; Tailwind build153ms; JS syntax clean |
| Deployment | Native Django/Python3.14 build READY; private production secret supplied through stdin; no database/env/local plan uploaded; Git auto-deploy disconnected |
| New browser checks | Unrun: physical touch, focus/layout, keypad JS/card delay, screen reader and Back-cache behavior require human browser rehearsal |

Two HTTP harness issues were corrected: comparing whole receipt HTML failed because
Django remasks CSRF inputs on each render; HTTPS POST initially omitted Referer and
Django correctly returned403. Harness now compares receipt facts and sends Referer.
These were test-harness fixes, not invented application bugs or disabled CSRF protection.
The local server on8000 was verified by workspace/manage.py command before restart.
Historical migrations/models/seed/tests were archived intact, not rewritten.
