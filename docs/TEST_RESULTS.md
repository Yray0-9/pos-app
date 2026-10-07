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
