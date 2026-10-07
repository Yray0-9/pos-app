# Common Table — local test and demonstration guide

Current completion is local/uncommitted on cart-review, based on f901b32. 21 database-free tests and live HTTP checks pass. New browser visual/touch/processing/history-cache checks require your own rehearsal; this guide is not evidence that you have already performed it. All payment methods are simulations.

## Open the checked preview

Use **http://127.0.0.1:8000/**. This is the completed preview. The verified old project process was restarted with the complete build. If needed, run from the project root:

```powershell
.\venv\Scripts\python.exe scripts/init_env.py
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

Skip starting a second server when8000 already works. Ctrl+C stops a server you launched in your terminal. If8000 is occupied by that preview, use it rather than killing another process. If Python/templates changed after a --noreload start, restart your own server. The initializer preserves an existing private environment; do not share its values. Catalog is fixed server code; no migrate/seed/database is needed.

## Five-minute transaction rehearsal

1. Start with an empty order. Review is disabled; direct payment must not let an empty order succeed.
2. Tap Chicken Rice Bowl twice, Chicken Wrap once and Cucumber Lemonade once. Check subtotals **170.00,70.00,39.50**, total **279.50**.
3. Increase rice to3: total **364.50**. Decrease to2: **279.50**. Remove lemonade: **240.00**. Add lemonade again: **279.50**. A decrease from1 removes a line; never a negative quantity.
4. Review. Check each name/unit price/quantity/subtotal/total. Back to selection must keep the order. Edit a quantity, then review again; the total must reflect the edit. Restore279.50 before the cash example.
5. Continue to Payment. Check Cash, QR Payment and Credit/Debit Card choices.
6. Cash: try blank, text, -1 and100. Each must show an error on payment with no success/receipt. Use the on-screen keypad; Clear and Exact amount should work. Try300: success total279.50, paid300.00, change20.50.
7. View Receipt. Check items/quantities/prices/subtotals, method Cash, paid/change, Asia/Singapore date/time and the same reference as success.
8. Tap New Transaction. Check empty cart/0.00 total. Browser Back/reload and direct old receipt URL must not reveal the previous active receipt. Only the active browser receipt is kept; reset clears it.
9. Add one Chicken Wrap and complete simulated QR: clear placeholder/instructions, total70.00, paid70.00, change0.00. Check receipt, then reset.
10. Add one Chicken Rice Bowl and complete simulated Card: total85.00; Process Payment should show a short processing state before success; paid85.00, change0.00. Check a different reference, then reset.
11. Run exact cash279.50 for the first example: change0.00. A serial repeated submit/reload must preserve the current receipt. Do not send real money or use real card details.

Local and public HTTP tests ran in isolated cookie jars and left no sales history. If your existing browser already has a paid order, use its receipt's New Transaction button before starting.

## Appearance and interaction checks still needed

- Desktop/tablet/narrow window: no horizontal overflow, long names/references wrap, total/actions remain readable; reach the full order and keypad by normal page scrolling.
- Tab/Shift+Tab/Enter: visible focus, useful reading order, reachable Back/Continue/keypad/payment/reset. Check zoom200% and a narrow window.
- Touch: product/quantity/remove and new payment controls feel comfortably large (source styles specify >=48px, new actions/keypad56px).
- Cash error is understandable, linked to its field, and you can correct it without losing the order. Card processing is visible; avoid double-taps producing duplicate success.
- Browser Back after reset reloads/checks active state rather than restoring the old receipt. Try a private/incognito window with the old receipt URL: it must not show that customer's receipt.
- No external Tailwind/font/CDN is needed. Browser source/loading must use local CSS/JS. Physical screen-reader/contrast checks are still pending.

Record your actual results and any error with the action/expected/observed behavior. Do not mark all these passed solely because backend tests pass. If appearance is unsatisfactory, describe the exact screen/spacing/control so the fix stays focused.

## Explain the implementation in your own words

| Topic | Explanation to understand, not a memorized answer |
| --- | --- |
| Project/app | pos_app holds global configuration; kiosk holds its catalog/calculation/views/templates/assets |
| Money | Server reads product prices; Decimal subtotal=price x quantity; total sums subtotals; change=paid-total |
| Navigation | Session IDs/quantities persist on ordinary GET/Back; edits invalidate payment confirmation |
| Stale order | Review/payment tokens must match current facts; empty/unavailable/edited orders cannot pay |
| Completion | Validate once and publish an active signed-cookie snapshot; serial retry keeps it, with no global lock |
| Receipt | Active purchased snapshot keeps original names/amounts until reset or cookie loss/expiry |
| Reset | Clear current browser state and change context; copied older signed cookies cannot be revoked |
| Simulation | QR/card do not contact a bank; JS processing is visible feedback, server checks are still required |
| AI/evidence | Explain what you requested, evaluated and actually adapted; do not claim teammate work, reviews or refactors that did not occur |

## Verification commands and limits

```powershell
.\venv\Scripts\python.exe manage.py test kiosk
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
pnpm run build:css
```

Use the bundled Node/pnpm fallback documented in README if those commands are not on PATH. A missing gh command is unrelated to running the kiosk. Git/account changes are not required for local testing. Do not change authors merely to add names.

Remaining exam evidence: your own evaluation/demo, other members' actual contributions/explanations, genuine PR review/feedback/merge, truthful committed-development/refactor audit, instructor access/clone verification and the final integration revision. Public website: https://common-table-kiosk.vercel.app. Main integration is requested. No grade or complete process compliance is guaranteed by this guide.

No-database replay/global-lock limits are documented and tested in DATA.md; ordinary browser reset is distinct from revoking an intentionally copied cookie.
