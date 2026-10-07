# Actual Vercel deployment

Production: https://common-table-kiosk.vercel.app
Deployment: dpl_CaAD2UzZwta8KY6YdfZCnAsYw1Z9
Inspect: https://vercel.com/yray0-9s-projects/common-table-kiosk/CaAD2UzZwta8KY6YdfZCnAsYw1Z9

2026-10-07: CLI62.4.0/Node24.19.0, authenticated yray0-9, dedicated project
common-table-kiosk in yray0-9s-projects. User approved normal device login. Local tested
files uploaded139.3KB/49files. Native Django preset detected6.1.2, Python3.14, installed
requirements, collected static files and completed10s build. Ready/production alias
confirmed. Ordinary public HTTPS acceptance passes Cash/QR/Card, real CSRF, receipt,
serial retry/reset/customer isolation and CSS/JS. This is a simulated kiosk, not banking.

Configuration: vercel.json framework=django; .python-version3.14; STATIC_ROOT=staticfiles;
production fresh DJANGO_SECRET_KEY as Vercel Secret, DJANGO_DEBUG=False,
DJANGO_ALLOWED_HOSTS=common-table-kiosk.vercel.app plus Vercel-generated exact hosts.
Secure session/CSRF cookies and trusted proxy HTTPS are enabled. No .env/key/token
contents appear here. .vercelignore excludes private/generated/test/docs/local-plan files.

The CLI linked Git automatically during project creation; this was deliberately
disconnected before deployment. Current main integration is separate; no push-triggered
publication of the older main/private files occurs. Production is a local-file deployment.
Future CLI redeploy after changes/checks:

```powershell
vercel deploy --prod --yes
```

On this machine the isolated tool lives in ignored tmp/vercel-cli/node_modules/.bin/vercel.cmd;
prepend the bundled Node path documented in README. A fresh computer can install the
official Vercel CLI and login normally. Keep production secret stable across redeploys
unless deliberately rotating sessions. Do not run env pull into tracked files.

There is no SQLite or persistent ledger. DATA.md explains cookie expiry/replay/global-lock
limits. Browser touch/focus/visible-processing checks, genuine member/review/history
evidence and final demonstrated Git SHA remain separate acceptance items.

Official setup: [Django on Vercel](https://vercel.com/docs/frameworks/full-stack/django),
[Python runtime/version](https://vercel.com/docs/functions/runtimes/python).

Git integration completed: normal main merge0764e08 pushed and verified; runtime diff with checked/deployed completion is empty. Cart-reviewc7cd068 also pushed. This evidence update changes documentation only; no unnecessary redeploy or claim of Git-triggered deployment. Current main excludes private and generated artifacts; historical commits retained.
