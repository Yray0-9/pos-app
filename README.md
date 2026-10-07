# Common Table - IT415 POS kiosk

A campus self-service kiosk project in progress. Accepted flow: choose products, review the order, select a payment method, complete simulated payment, view a digital receipt, and start a new transaction.

**Current milestone:** Prompt 06 selection/cart implementation [f901b32](https://github.com/Yray0-9/pos-app/commit/f901b32620a3a53c298664f945813bf34f34cf28) committed/pushed on cart-review; [PR #4](https://github.com/Yray0-9/pos-app/pull/4) open/unmerged into catalog-data (base 796b5da). All 24 tests and configuration/dependency/migration/JavaScript/scope checks passed. Genuine review pending; quota-only bot COMMENTED notice, no inline/discussion findings or CI checks/statuses. Next numbered stage: Prompt 07 on the same cart-review branch after inspecting/reusing its state. No new branch, merge, deployment, reviewer contact or automatic feature work. Review/payment/receipt/reset remain unimplemented; F07-F08 are pending.

## Course and group

- Instructor: Reban Cliff A. Fajardo, MIT.
- Shared repository: [Yray0-9/pos-app](https://github.com/Yray0-9/pos-app).
- M1 - Agbas; M2 - Daro; M3 - Magos (current user).
- User-supplied deadline: October 7, 2026, 9:00 PM Asia/Singapore.
- Group name/number, section, evaluation date, and individual GitHub usernames: pending.

See [member register](docs/MEMBER_REGISTER.md) for actual evidence and unverified items. Names listed here are group membership, not claims of authored features.

## Verified environment and stack

Python 3.14.4 and Django 6.1.2 were observed in the existing Windows virtual environment. All currently installed application packages are pinned in `requirements.txt`; pip itself is tooling and is not a runtime requirement. `python-dotenv` loads the private environment file.

The agreed architecture is Django templates, locally built Tailwind CSS, modest JavaScript, SQLite product/completed-sale records and a Django session cart. The cart stores product IDs and integer quantities; Django calculates money using current database prices and Python Decimal. JavaScript replaces server-rendered workspace HTML after an action; native forms also work. Completed sale snapshots belong to later payment stages and outlive the active cart.

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

Prompt 05 applied the new kiosk migration and Django's standard dependency migrations. Before running a fresh prepared checkout, run `manage.py migrate` and `manage.py seed_catalog` as shown below. No superuser, customer login or custom admin feature has been created.

## Template and static-file responsibilities

`pos_app` is the Django **project**: global settings and top-level routes. `kiosk` is the Django **app**: models, catalog/cart calculation, views, templates and assets. The root GET loads available products and reads the session cart without changing its contents. The CSRF-protected /cart/ POST route applies order edits.

- `kiosk/templates/kiosk/base.html`: shared document, branding, stylesheet link, progress slot, messages, main content, and footer. Future screens extend its content block.
- `kiosk/templates/kiosk/home.html`: includes the live workspace and original SVG symbols, with the cart JavaScript asset. The workspace/product-card includes render database-backed cards and the current order. Review stays disabled until Prompt 07.
- `kiosk/templates/kiosk/components/`: reusable progress, escaped feedback/messages, product_card.html, workspace.html and original inline menu_art.html SVG symbols. The obsolete disabled fixture template was removed. All displayed order money comes from server context.
- `kiosk/assets/input.css`: editable Tailwind source and shared controls. Edit this rather than the generated stylesheet.
- `kiosk/static/kiosk/`: namespaced browser assets, including built CSS and our own SVG favicon and decorative campus-food illustration. Django's `{% static %}` resolves these files; `runserver` serves them during local DEBUG development. Production static serving is outside this stage.

The progress list is informational with Choose marked current. It has no fake navigation links. Decorative artwork is static, focus outlines are visible, and reduced-motion preferences are respected. JavaScript restores focus after order updates and serializes actions within this page; cross-tab/session concurrency is not guaranteed.

## Checks and future build steps

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
```

The actual results and limitations are in [TEST_RESULTS.md](docs/TEST_RESULTS.md). All 24 data/cart tests passed, along with configuration/dependency/migration checks and the local CSS build. Browser selection, quantity/removal arithmetic, reload persistence, keyboard focus, touch sizes and desktop/tablet/narrow overflow were checked. Payment/receipt/reset and full exam acceptance remain pending.

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

Working catalog selection and a server-calculated session cart now exist. Order review/checkout, payment, receipt and reset remain unimplemented. Review is disabled for both empty and nonempty carts during this stage; Prompt 07 must also reject empty orders at its endpoint. All eventual payments are simulated. Inventory, login, reports, discounts, printing and deployment remain outside initial scope. Actual member contributions, explanations and genuine review remain pending.

Prompt 04 implementation: [6ff4a07](https://github.com/Yray0-9/pos-app/commit/6ff4a07cbc410b3436c6f6e2c4ed152fac33977b), on codex/ui-foundation. [UI PR #2](https://github.com/Yray0-9/pos-app/pull/2) targets codex/setup-foundation and remains unmerged. The cart checkpoint is now complete in PR #4. **Next numbered stage: Prompt 07, reusing cart-review after checking its actual state.**


The historical UI workspace revision removed the large hero and adapted the sample menu/order organization using our own theme/artwork. Prompt 06 connects that layout to real products/cart state. [Current cart screenshot](docs/evidence/cart-desktop.jpg); [historical UI preview](docs/evidence/ui-foundation-workspace-desktop.jpg). Magos requested the current milestone; personal visual acceptance and instructor approval are not inferred.


The UI branch is now remotely available for review. After cloning, use `git switch --track origin/codex/ui-foundation` if no local UI branch exists, or `git switch codex/ui-foundation` if it does. These are instructions, not a claimed fresh-clone demonstration. A non-author reviewer should inspect PR #2 and verify the stated foundation checks, then leave actual feedback before an authorized merge. Both setup and UI PRs remain unmerged.

## Catalog branch preparation and integration issue

Reusable E initially created `codex/catalog-data`. Following Magos's naming/commit request, the evidence records were committed on UI as `3ce83e2`; an unused local task branch was replaced with `catalog-data` from that updated base. The later explicitly requested B checkpoint pushed that UI parent and catalog implementation `a02288b`, then opened [PR #3](https://github.com/Yray0-9/pos-app/pull/3). No merge occurred.

Fresh GitHub inspection confirmed public main at `141af01` tracks `.env` and generated package/cache artifacts while omitting prepared application sources. It was left untouched and was not used as the catalog base. The current local development key differs from the tracked key; no values are included in evidence. Cleanup of the published private file/history and application integration remain separate unresolved work, with no history rewriting authorized by this checkpoint.

## Data setup and verification

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py seed_catalog
.\venv\Scripts\python.exe manage.py test kiosk
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Read [DATA.md](docs/DATA.md) for every stored field, money/quantity limits, storage guarantees and the planned shared calculation/completion flow. Seed again safely: it creates only missing agreed products and preserves IDs, custom edits, unrelated records and sales. The local database is ignored; commit migrations and seed code instead. Test sales use a separate in-memory database.

The UI evidence commit 3ce83e2 and catalog implementation a02288b are now pushed. Catalog PR #3 is open/attached and needs genuine non-author review; Copilot's quota comment is not approval. Future simple task names/grouping are recorded in BUILD_PROMPTS.md; six feature branches plus main are proposed, not a fixed rubric requirement or completed member record.

## Try the selection milestone

Open localhost and tap Chicken Rice Bowl twice, Chicken Wrap once and Cucumber Lemonade once. The line subtotals are PHP 170.00, 70.00 and 39.50; total PHP 279.50. Increase the rice bowl to three: total PHP 364.50. Decrease returns to PHP 279.50; remove lemonade gives PHP 240.00. Decreasing a one-item line removes it. Explicit Remove deletes the whole line. Reload keeps the active order.

Each item permits quantities 1-99. Direct quantity/price/total submissions are ignored: actions change quantities by one and use database money. Invalid actions/products and attempts to exceed the limit show feedback without changing the order. Damaged or unavailable saved entries show a warning and are excluded from the displayed total; Update order explicitly repairs the cart. A valid cart edit also removes those entries with feedback. GET does not silently rewrite them.

The saved screenshot captures two rice bowls, one wrap and one lemonade (PHP 279.50); the live cart can change through further interaction. No completed sale was created. To clear this demonstration order, use its Remove controls. Customer reset, receipt ownership and payment idempotency are future work.

Run manage.py test kiosk for data/cart checks. Rebuild CSS after template/CSS changes. Restart the --noreload development server after Python changes. Current server was restarted and remains running on 127.0.0.1:8000.

## Selection/cart Git checkpoint

Implementation [f901b32](https://github.com/Yray0-9/pos-app/commit/f901b32620a3a53c298664f945813bf34f34cf28) is pushed on [cart-review](https://github.com/Yray0-9/pos-app/tree/cart-review), with [PR #4](https://github.com/Yray0-9/pos-app/pull/4) open into catalog-data. Configured author Romulo Magos retained; authenticated publisher Yray0-9. Actual evidence is in MEMBER_REGISTER.md and TEST_RESULTS.md. A documentation-only follow-up records returned links/status.

The [bot quota comment](https://github.com/Yray0-9/pos-app/pull/4#pullrequestreview-5440581047) is not approval. A genuine non-author reviewer (Agbas/Daro with confirmed account, or an instructor-accepted reviewer) must inspect the diff, verify the stated behavior and provide actual feedback. No reviewer contacted and no merge. Other member feature contributions and individual explanations remain pending. Next: Prompt 07 on the same branch after state inspection; no new branch is necessary merely because the prompt number changes.
