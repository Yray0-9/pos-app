# Common Table - IT415 POS kiosk

A campus self-service kiosk project in progress. Accepted flow: choose products, review the order, select a payment method, complete simulated payment, view a digital receipt, and start a new transaction.

**Current milestone:** Prompt 03 foundation and evidence records. The kiosk app, HTML screens, Tailwind CSS, catalog, payments, and receipts have not been implemented. Only the Django scaffold is available; do not treat it as a completed POS.

## Course and group

- Instructor: Reban Cliff A. Fajardo, MIT.
- Shared repository: [Yray0-9/pos-app](https://github.com/Yray0-9/pos-app).
- M1 - Agbas; M2 - Daro; M3 - Magos (current user).
- User-supplied deadline: October 7, 2026, 9:00 PM Asia/Singapore.
- Group name/number, section, evaluation date, and individual GitHub usernames: pending.

See [member register](docs/MEMBER_REGISTER.md) for actual evidence and unverified items. Names listed here are group membership, not claims of authored features.

## Verified environment and stack

Python 3.14.4 and Django 6.1.2 were observed in the existing Windows virtual environment. All currently installed application packages are pinned in `requirements.txt`; pip itself is tooling and is not a runtime requirement. `python-dotenv` loads the private environment file.

The agreed architecture is Django templates, locally built Tailwind CSS, modest JavaScript, SQLite product/completed-sale records, and a Django session cart. Only configuration exists at this stage. SQLite suits this local exam demonstration because it needs no separate database service. The cart will hold active state; completed sale snapshots will preserve receipt values. Money calculations will use Python Decimal. These models and behaviors remain future work.

## Set up on Windows PowerShell

Run commands from the repository root. If starting on another computer, obtain access to the shared repository, then clone it:

```powershell
git clone https://github.com/Yray0-9/pos-app.git
Set-Location pos-app
```

Cloning is an instruction, not a claim that the group has demonstrated cloning. Setup is available on the `codex/setup-foundation` branch in [PR #1](https://github.com/Yray0-9/pos-app/pull/1), which is not merged into main yet. For reviewing this milestone after cloning, use `git switch --track origin/codex/setup-foundation` if no local branch exists; use `git switch codex/setup-foundation` if it already exists. Do not assume main contains the setup before review/merge.

For a new local environment with Python 3.14 installed:

```powershell
py -3.14 -m venv venv
```

Skip environment creation if the existing `venv` is already working. Invoke its Python directly; activation and execution-policy changes are unnecessary:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe scripts/init_env.py
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
```

`init_env.py` creates an ignored `.env` with a fresh secret and the safe development settings from `.env.example`. It preserves an existing `.env` without printing values. Django also accepts real environment variables, which take precedence. A missing `DJANGO_SECRET_KEY` raises a clear setup error. Do not add `.env` or its values to commits, screenshots, or evidence logs.

The template enables local development debugging and localhost hosts. It is not production configuration. Time display is configured for Asia/Singapore.

## Run the current scaffold

```powershell
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

Open [localhost](http://127.0.0.1:8000/). At this milestone, the debug scaffold may show Django's default welcome page; it is not the kiosk. `/admin/` is the only configured route. Stop the server with Ctrl+C.

No migrations have been applied in Prompt 03. Admin login and database-backed sessions are not ready until the later authorized migration/setup stage. Do not run migration commands solely from this document during Prompt 03.

## Checks and future build steps

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
```

The actual results and limitations are in [TEST_RESULTS.md](docs/TEST_RESULTS.md). There are no kiosk feature tests yet. `manage.py test`, model migrations, product seeding, and Tailwind install/build commands will be added when those features/tooling exist and have been verified. Do not assume commands or dependency versions for future work.

## Development and evidence workflow

1. Use one scoped prompt from [BUILD_PROMPTS.md](docs/BUILD_PROMPTS.md).
2. Establish the actual contributor's feature branch before editing once Git changes are explicitly requested.
3. Implement that milestone, verify it, and record prompts/responses, evaluations, adaptations, and observed results.
4. Record a meaningful commit, push the branch, and open a feature PR through the Git checkpoint prompt.
5. Obtain genuine review before merge; resolve actual feedback and record the reviewer and merge.
6. Keep at least seven real development stages visible across setup, interface, core functionality, validation, bug fix, refactoring, and documentation. Do not manufacture bugs, refactoring, commits, or member authorship to meet the checklist.
7. Record and demonstrate the actual final integration commit.

The existing initial commit does not establish all stages. Prompt 03 itself made no Git mutations; the subsequent explicitly authorized checkpoint committed/pushed the scaffold and setup as [a20201a](https://github.com/Yray0-9/pos-app/commit/a20201aeb262959b4d38f5f80bed78a3b5e8d56f) on `codex/setup-foundation` and opened [PR #1](https://github.com/Yray0-9/pos-app/pull/1) into main. A documentation update records the checkpoint evidence on the same branch. PR review/merge, instructor access, other member identities, cloning demonstration, and individual contribution explanations remain pending. No merge or deployment was performed.

## Documentation

- [EXAM_PLAN.md](docs/EXAM_PLAN.md): requirements, scope, acceptance checklist, and status.
- [DESIGN.md](docs/DESIGN.md): accepted original direction and detailed behavior specifications.
- [BUILD_PROMPTS.md](docs/BUILD_PROMPTS.md): one-stage prompts and Git checkpoints.
- [AI_LOG.md](docs/AI_LOG.md): actual prompts/responses, assistance, evaluations, adaptations, and gaps.
- [MEMBER_REGISTER.md](docs/MEMBER_REGISTER.md): repository/member/PR evidence and individual verification matrix.
- [TEST_RESULTS.md](docs/TEST_RESULTS.md): checks performed and remaining acceptance tests.

The new Acceptance Checklist PDF requires functional checks, shared-repository evidence, and individual process verification. Our records support completing that form later; its Pass/Fail and instructor-verification fields are not automatically marked by this README. Word/PDF report requirements, if separately assigned, still need confirmation.

## Current limitations

No working products, cart, checkout, payment, receipt, reset, or Tailwind/HTML interface exists yet. All eventual payments will be simulated; no real money or card credentials are required. Inventory, login, reports, discounts, receipt printing, and deployment are outside the initial scope. Group contributions and reviews must be backed by actual activity and each member's understanding.
