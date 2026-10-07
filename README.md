# Common Table — IT415 touchscreen POS kiosk

A Django campus kiosk with six products, editable cart, order review, Cash/QR/Card
simulations, success, digital receipt and New Transaction. All amounts are PHP.

**Public website:** https://common-table-kiosk.vercel.app
**Checked local preview:** http://127.0.0.1:8000/
**Current storage:** no database. Fixed server catalog and signed-cookie active state.
21 automated tests pass; local and public HTTP acceptance pass. Browser touch/layout
checks and genuine group/review/history evidence remain pending. Completion is integrated/pushed to main through normal merge [0764e08](https://github.com/Yray0-9/pos-app/commit/0764e0815e1b6f678e1c9c6b2e4a2de2e577931c). See MEMBER_REGISTER.md for actual Git outcomes.

## Run on Windows

From the project root with Python 3.14:

```powershell
py -3.14 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe scripts/init_env.py
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

Skip environment creation if the existing venv works. The initializer preserves an
existing private .env; it never prints the key. Environment variables take precedence.
No migrations, database, seeding, superuser or login are needed. Ctrl+C stops your
server; restart after Python/template edits when using --noreload. Refresh the page
if an older server previously showed “Payment is not available yet”. Do not kill an
unrelated server. Local .env must remain private and ignored.

## Build local Tailwind CSS

Verified Node 24.19.0, pnpm 11.19.0, Tailwind/CLI 4.3.3. Direct dependencies and lockfile
are pinned. Initial installation needs internet; evaluation uses built local CSS/JS/SVG
and system fonts with no CDN dependency.

```powershell
pnpm install --frozen-lockfile
pnpm run build:css
```

On this computer, bundled tooling is available if pnpm/node are absent from PATH:

```powershell
$env:PATH = 'C:\Users\Romul\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin;' + $env:PATH
& 'C:\Users\Romul\.cache\codex-runtimes\codex-primary-runtime\dependencies\bin\fallback\pnpm.cmd' run build:css
```

Tailwind v4 input kiosk/assets/input.css registers ../templates using @source; palette
uses @theme. CSS output kiosk/static/kiosk/css/app.css is kept with the app. Use
pnpm run watch:css while editing. Browser runtime does not need Node or pnpm.

## How it works

- pos_app is the Django project: configuration, WSGI and top-level routes.
- kiosk is the app: fixed catalog, shared Decimal calculation, views and templates.
- Templates render validated server data. Static CSS styles it; small JavaScript adds
  cart refresh, cash keypad, 1.2-second card processing feedback and Back-cache reload.
- Catalog prices come from kiosk/catalog.py, never browser money. Subtotal is unit
  price × quantity; total sums subtotals; cash change is paid − total. Quantity 1–99;
  decrease from one removes the line; Remove deletes it explicitly.
- Review binds current order facts; Back preserves the session cart. Edits invalidate
  confirmation. Missing/unavailable items require explicit repair before checkout.
- Cash rejects missing/text/negative/non-finite/insufficient/excess-precision values.
  QR shows a non-scannable demo placeholder and Confirm Payment. Card shows reader
  instructions/processing. No real financial service or card information is involved.
- Completion stores one active receipt snapshot in the signed cookie: names, prices,
  quantities/subtotals, timestamp, total, paid/change, method and distinct reference.
  Serial retries preserve it. Once paid, selection redirects to the receipt until reset.
- New Transaction starts empty, removes active receipt/payment facts and changes
  customer context. Separate ordinary browser sessions cannot read each other's receipt.

**No-database limits:** there is no permanent sales history. Signed cookies are authentic,
not encrypted; copied old cookies cannot be revoked by reset until expiry. Separate
precompletion cookies cannot enforce global exactly-once completion for conflicting
simultaneous requests. This is a simulated exam kiosk, not a payment gateway. Do not
claim durable ledger/charge guarantees. See [DATA.md](docs/DATA.md).

## Verify and rehearse

```powershell
.\venv\Scripts\python.exe manage.py test kiosk
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py collectstatic --noinput
```

SimpleTestCase forbids database queries; current suite runs 21 tests. Read
[DEMO_GUIDE.md](docs/DEMO_GUIDE.md) for your personal touch, appearance, cash, QR/card,
receipt and reset rehearsal. Original SQLite model/migration/seed/tests are inactive
history in docs/archive/sqlite-foundation; do not run them. Old 46-test evidence applies
only to the removed SQLite architecture.

## Deployment and evidence

[DEPLOYMENT.md](docs/DEPLOYMENT.md) records the actual Vercel deployment and commands.
Vercel native Django preset detects manage.py/WSGI, uses Python 3.14 and requirements.txt,
and collects static files. Production uses a fresh private Vercel signing secret,
DEBUG=False, validated hosts and secure cookies. .vercelignore excludes environment
files, local tools/plan, databases, venv, node_modules and docs. No private plan was
uploaded or pushed. Automatic Git deployment is disconnected; main integration is now pushed and its runtime matches the deployed build. Deployment used tested local files; a live URL is not proof of
an integrated Git commit or instructor approval.

Instructor: Reban Cliff A. Fajardo, MIT. Members: M1 Agbas, M2 Daro, M3 Magos.
Requester/implementation work is Magos with AI assistance; other members' work is
unverified. Group/section details, real independent review, individual explanations,
seven actual committed stages and instructor access remain to verify. Do not fabricate
names or reviews. See EXAM_PLAN, AI_LOG, MEMBER_REGISTER and TEST_RESULTS under docs.
