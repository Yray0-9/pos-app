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
