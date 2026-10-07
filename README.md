# Common Table - IT415 POS kiosk

A campus self-service kiosk project in progress. Accepted flow: choose products, review the order, select a payment method, complete simulated payment, view a digital receipt, and start a new transaction.

**Current milestone:** Prompt 04 UI foundation, checked on `codex/ui-foundation` and being recorded for review through Magos's explicitly requested Git checkpoint. The Common Table page includes the requested modern visual revision. Reusable Django templates, local Tailwind build, keyboard access, and responsive spacing exist. Catalog, cart, payments, receipt, and reset remain future work; this is not a completed POS.

## Course and group

- Instructor: Reban Cliff A. Fajardo, MIT.
- Shared repository: [Yray0-9/pos-app](https://github.com/Yray0-9/pos-app).
- M1 - Agbas; M2 - Daro; M3 - Magos (current user).
- User-supplied deadline: October 7, 2026, 9:00 PM Asia/Singapore.
- Group name/number, section, evaluation date, and individual GitHub usernames: pending.

See [member register](docs/MEMBER_REGISTER.md) for actual evidence and unverified items. Names listed here are group membership, not claims of authored features.

## Verified environment and stack

Python 3.14.4 and Django 6.1.2 were observed in the existing Windows virtual environment. All currently installed application packages are pinned in `requirements.txt`; pip itself is tooling and is not a runtime requirement. `python-dotenv` loads the private environment file.

The agreed architecture is Django templates, locally built Tailwind CSS, modest JavaScript, SQLite product/completed-sale records, and a Django session cart. Templates and CSS now exist; no JavaScript is needed for this foundation. SQLite suits this local exam demonstration because it needs no separate database service. The cart will hold active state; completed sale snapshots will preserve receipt values. Money calculations will use Python Decimal. These models and behaviors remain future work.

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

## Build the local styles

Observed tooling: Node.js 24.19.0, pnpm 11.19.0, Tailwind CSS and CLI 4.3.3. `package.json` pins direct CSS dependencies; `pnpm-lock.yaml` records resolved dependencies. Use Node 24 and pnpm 11.19.0, then run from the repository root:

```powershell
pnpm install --frozen-lockfile
pnpm run build:css
```

Internet is needed for the initial package download. The resulting `kiosk/static/kiosk/css/app.css` is deliberately kept in source control at the Git checkpoint, so the evaluation page uses local CSS without downloading Tailwind or fonts at runtime. Do not commit `node_modules` or the package cache. When editing templates or source CSS, run `pnpm run watch:css` in a separate interactive terminal; stop with Ctrl+C, then run `pnpm run build:css` for the final minified file.

This computer currently exposes pnpm through Codex's bundled path rather than a normal PATH entry. The actual verified command prefix here is:

```powershell
& 'C:\Users\Romul\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd' install --frozen-lockfile
& 'C:\Users\Romul\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd' run build:css
```

Use ordinary `pnpm` on a computer where it is installed on PATH. Automated terminals may use `$env:CI = 'true'` for a noninteractive install. The locked install was also verified using `--offline` after the packages had been downloaded; a fresh clone/install on another computer remains untested.

Tailwind v4 uses CSS configuration: `kiosk/assets/input.css` declares the palette/typeface with `@theme`, disables broad scanning with `source(none)`, and registers `../templates` with `@source`. This detects literal classes inside Django templates and includes; no v3 `tailwind.config.js` is required. Add explicit source paths if JavaScript later contains classes. Keep full class names literal. `pnpm-workspace.yaml` deliberately skips the Parcel watcher source-build script; the downloaded platform-specific prebuilt watcher worked in the Windows watch verification.

References: [official Tailwind CLI instructions](https://tailwindcss.com/docs/installation/tailwind-cli), [source detection](https://tailwindcss.com/docs/detecting-classes-in-source-files), and [pnpm 11 build policy](https://pnpm.io/blog/releases/11.0).

## Run the current foundation

```powershell
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

Open [localhost](http://127.0.0.1:8000/). `/` serves the Common Table foundation; `/admin/` remains the standard Django admin route. Stop the server with Ctrl+C. Build CSS before starting the server. If a new static directory was created after starting with `--noreload`, restart the server so Django discovers it. Styling itself can be rebuilt and viewed after a browser reload. With `--noreload`, template edits may also require a server restart because the template loader caches them; restart when the old HTML persists.

No migrations have been applied in Prompt 03. Admin login and database-backed sessions are not ready until the later authorized migration/setup stage. Do not run migration commands solely from this document during Prompt 03.

## Template and static-file responsibilities

`pos_app` is the Django **project**: global settings and top-level routes. `kiosk` is the Django **app**: the kiosk route/view and related templates/assets. The root view only renders HTML; it does not access a cart or database.

- `kiosk/templates/kiosk/base.html`: shared document, branding, stylesheet link, progress slot, messages, main content, and footer. Future screens extend its content block.
- `kiosk/templates/kiosk/home.html`: the current menu-unavailable and empty-order foundation. Review is truly disabled. The native disclosure explains the future flow without JavaScript.
- `kiosk/templates/kiosk/components/`: reusable progress, escaped feedback, and Django message rendering. Error feedback uses `alert`; informational/success/loading feedback uses `status`; loading includes `aria-busy`. These variants were rendered in verification, not connected to invented transactions.
- `kiosk/assets/input.css`: editable Tailwind source and shared controls. Edit this rather than the generated stylesheet.
- `kiosk/static/kiosk/`: namespaced browser assets, including built CSS and our own SVG favicon and decorative campus-food illustration. Django's `{% static %}` resolves these files; `runserver` serves them during local DEBUG development. Production static serving is outside this stage.

The progress list is informational, with no fake links. No transaction is active, so none of its steps is marked current on the foundation page. Future views can supply the verified current step. Decorative artwork is static, focus outlines are visible, and reduced-motion preferences are respected in the CSS.

## Checks and future build steps

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
```

The actual results and limitations are in [TEST_RESULTS.md](docs/TEST_RESULTS.md). Foundation checks include HTTP/CSS delivery, deterministic CSS builds, watcher updates, feedback escaping/semantics, keyboard focus, and desktop/tablet/narrow-screen overflow. No transaction acceptance test is claimed. Model migrations, seeding, and feature tests remain for their authorized stages.

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

No working products, cart, checkout, payment, receipt, or reset exists yet. All eventual payments will be simulated; no real money or card credentials are required. Inventory, login, reports, discounts, receipt printing, and deployment are outside the initial scope. Group contributions and reviews must be backed by actual activity and each member's understanding.

Prompt 04 uses `codex/ui-foundation`, based on setup head `717b165`. Setup PR #1 remains open. Magos explicitly delegated this UI commit/push/PR checkpoint after the design revision; subsequent Git operations still need their authorization. The UI PR targets `codex/setup-foundation` while setup is unmerged, and genuine review/integration remains pending. **Next numbered stage: Prompt 05, catalog and transaction data foundations, after feature branch preparation.**


The current revision uses a darker hero, stronger wordmark/type, restrained lime accents and original SVG food artwork, with compact menu and order surfaces. The menu is still explicitly unavailable. [Current design preview](docs/evidence/ui-foundation-modern-desktop.jpg). Magos subsequently requested this completed milestone be recorded for review; this is not an instructor approval or a claim of independent teammate review.
