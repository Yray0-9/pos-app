# Common Table: proposed kiosk design and transaction behavior

Prepared: 2026-10-07 (Asia/Singapore). Prompt 02 planning output.

## Status and assignment context

**Current visual direction:** Section 13 is the user-requested menu-and-order workspace. It replaces the large hero and earlier full-width order layout. Magos has requested the next feature branch; the workspace is in existing UI commit 3cad483. Detailed human evaluation remains unrecorded. Earlier sections preserve history and do not override section 13's layout.

The user accepted the proposed design direction on 2026-10-07: Common Table, cream/green/plum colors, the six-product catalog, products above a full-width order list, and SQLite with a session cart. This is the accepted planning baseline, not an implemented interface. Detailed interaction/data policies below remain design specifications to verify during implementation. No screens, models, migrations, dependencies, or Git operations were created by this stage. The customer workflow follows `docs/EXAM_PLAN.md`; the professor's sample UI is a behavioral reference only.

User-supplied details:
- Instructor: Reban Cliff A. Fajardo, MIT.
- Intended repository: https://github.com/Yray0-9/pos-app (access and permissions not verified at this stage).
- Members: M1 - Agbas; M2 - Daro; M3 - Magos.
- Current user: M3 - Magos. User-supplied deadline: 2026-10-07 at 21:00 Asia/Singapore ("later 9pm").
- Individual GitHub usernames and separate submission rules remain unconfirmed. Names do not establish completed contributions or task acceptance.

Confirmed preferences: original design, modern and calm, Django foundation, Tailwind permitted, step-by-step development. Accepted direction: Common Table name, palette, six-product catalog, layout, SQLite records, and session cart. Detailed implementation policies remain subject to verification and any necessary documented refinement.

## 1. Proposed identity and visual direction

**Store name:** Common Table.
**Customer-facing description:** Campus bites and everyday favorites.
**Tone:** friendly, clear, quiet, and practical. No claim of trademark clearance or exclusive use of the name.

Use a light warm canvas, dark green text/actions, soft sage state surfaces, and a restrained plum accent. Product names and prices are the main visual content. No required photography, oversized decorative payment illustrations, category filters, or animation-heavy transitions. Small original line symbols may support labels; controls remain understandable without them.

Originality decisions: no copied navy/orange theme, logo, product artwork or receipt illustration. The original proposal used products above a full-width order list. Magos subsequently requested the sample's workspace organization; section 13 now specifies the desktop menu beside an order panel. Common quantity controls and cash keypads remain familiar for usability.

### Color tokens

| Token | Value | Use |
| --- | --- | --- |
| Canvas | `#F7F5EF` | Warm page background |
| Surface | `#FFFFFF` | Product cards, order rows, input surfaces |
| Main text | `#24342E` | Headings, product names, amounts |
| Secondary text | `#5C6962` | Supporting descriptions and labels |
| Primary | `#24584B` | Main actions, selected borders, focus outline |
| Soft green | `#E7F0E8` | Selection/success support surfaces |
| Accent | `#5C496E` | Small section labels or reference details |
| Error | `#A13632` | Error text and icons |
| Error surface | `#FFF1EF` | Inline validation background |
| Decorative line | `#DADFD6` | Nonessential dividers; not the only control boundary |

Calculated sRGB contrast checks for proposed solid colors: main text/canvas 12.00:1; secondary text/white 5.75:1; white/primary 8.16:1; error/error surface 6.18:1; primary/soft green 7.01:1; accent/canvas 7.32:1. These are token calculations, not a claim of complete accessibility compliance. Recheck actual rendered states, overlays, input borders, icons, and focus during implementation. Aim for at least 4.5:1 for ordinary text and 3:1 for large text and required non-text indicators.

### Typography, spacing, and controls

- Use a locally available system sans stack: `Segoe UI`, system UI, sans-serif; no online font dependency. Use tabular numerals for aligned quantities and money.
- Main page title: about 32px desktop / 28px tablet. Section titles: 22-24px. Body/product names: 18px. Secondary labels: 16px. Large total: 28-32px. Receipt line items: at least 16px.
- Spacing rhythm: 4, 8, 12, 16, 24, 32px. Content max-width about 1120px with 24-32px desktop gutters and 16-24px tablet gutters.
- Product cards: approximately 160px minimum height; entire card is a labeled button. Buttons and inputs: at least 48px high; important actions 56px. Quantity/keypad buttons: at least 52px square with at least 8px separation.
- Corners: around 16px for larger cards, 12px for controls. Use borders and very light shadow sparingly.
- One dominant action per screen. Back is a labeled secondary action. Removal has an explicit accessible product name and a visible label; no tiny trash icon as the only target.
- Focus: visible 3px primary outline with offset; never removed without replacement. Selection uses border, text, and quantity, not color alone.
- Buttons, form labels, errors, and headings use semantic HTML. Native buttons work with Enter/Space; inputs support typing as well as the touchscreen keypad. Tab order follows reading order. Status feedback is announced politely; actionable errors are associated with their input.
- Reduced-motion preference removes decorative motion. Card processing still communicates status in text. A short processing interval is proposed, about one second, and is not proof of real bank activity.

The 48px target is our design goal. Do not describe it as the exact WCAG 2.2 AA minimum, which has its own 24px criterion and exceptions.

## 2. Proposed six-product catalog

All names and prices are our proposal, independent of the professor's example catalog. Currency is Philippine pesos; show two decimal places consistently. No inventory values or category filtering required.

| Seed key | Name | Price | Short display description |
| --- | --- | --- | --- |
| rice-bowl | Chicken Rice Bowl | PHP 85.00 | A warm campus lunch |
| chicken-wrap | Chicken Wrap | PHP 70.00 | A quick savory bite |
| cucumber-lemonade | Cucumber Lemonade | PHP 39.50 | A refreshing cool drink |
| banana-muffin | Banana Muffin | PHP 34.50 | A soft baked snack |
| cheese-bun | Cheese Bun | PHP 29.50 | A light savory snack |
| granola-pack | Granola Pack | PHP 24.00 | An easy takeaway snack |

Stable seed keys allow repeatable seeding without duplicating products. Short descriptions are optional design content, not professor requirements. All six remain selectable in the baseline.

Equivalent calculation example for verification: rice bowl x2 = 170.00, wrap x1 = 70.00, lemonade x1 = 39.50; total = 279.50. Rice x3 changes total to 364.50; reducing back gives 279.50. Removing lemonade gives 240.00. Paying 200.00 for that order fails with a 40.00 shortfall; 300.00 succeeds with 60.00 change; 240.00 succeeds with zero change. QR/card paid = 240.00 and change = 0.00. These are planned expected results, not executed tests.

## 3. Original layout and responsive behavior

### Historical selection proposal: products above a full-width order list

This earlier text wireframe is retained as planning history; section 13 replaces its layout. It is not the current screen:

```text
+------------------------------------------------------------+
| Common Table                         Step 1 of 4: Choose    |
| Campus bites and everyday favorites                         |
+------------------------------------------------------------+
| Choose your favorites                                      |
| [Rice bowl       85.00] [Wrap 70.00] [Lemonade 39.50]        |
| [Muffin          34.50] [Bun  29.50] [Granola  24.00]        |
+------------------------------------------------------------+
| Your order                                                 |
| Product       Unit price     [-] Qty [+]   Subtotal Remove  |
| ...                                                        |
+------------------------------------------------------------+
| 4 items                         Total 279.50 [Review order] |
+------------------------------------------------------------+
```

The customer-facing four milestones are Choose, Review, Pay, Receipt. They group the exam's seven actions without omitting payment processing, success, or reset. Use a plain text step label and lightweight progress line rather than the sample's pill navigation. Future steps are informational, not links that bypass payment.

- Desktop (about 1024px and above): three product columns; order list spans the content width below them. Only the compact total/action bar is sticky at the bottom. The full order list remains in normal page flow, not a permanently fixed tall panel.
- Tablet (about 768-1023px): two product columns; wider touch rows; content scrolls naturally. Show every cart value; wrap rows instead of hiding unit price or subtotal.
- Narrow fallback (below about 768px): one or two columns based on actual readable card width; cart rows become labeled blocks; actions stack if necessary.
- Add bottom padding so the sticky bar never covers the final cart row or focus target. Use one vertical page scroll, avoid nested cart scrolling, and keep operation usable at 200% zoom. Exact breakpoints are implementation decisions to verify.
- Initial empty order: short instruction, total 0.00, disabled Review order with explanatory text. Successful product addition announces the item and updates its selected quantity marker and order list.

### Other screens

| Screen / exam action | Proposed arrangement | Main action / required behavior |
| --- | --- | --- |
| Review | Wide readable order list with price/quantity/subtotal columns; total strip below | Back to selection preserves values; Continue to payment |
| Payment choice | Amount due above three labeled, text-led method cards | Select Cash, QR Payment, or Credit/Debit Card; Back to review |
| Cash | Entry + keypad as the main column; compact confirmed-order facts alongside on desktop, below on tablet | Pay now; inline amount error; change preview; change method |
| QR | Amount and scan instructions above a clearly labeled simulated QR placeholder | Confirm payment; change method; never imply a live banking code |
| Card | Amount, tap/insert/swipe instruction, and simple processing status region | Process payment; then visible processing and server-confirmed completion |
| Success | Full-width success banner and a structured transaction detail list | View receipt; show amount, paid, change, method, reference |
| Receipt | Wide clean digital invoice with readable line items and totals, not a thermal-paper illustration | New transaction; date/reference, items, quantities, prices/subtotals, method, paid, change |
| Reset | Return to the selection empty state | Clear old active details, show brief New transaction feedback |

Required receipt data are preserved even though its visual shape differs from the sample. No Print Receipt action in the baseline.

## 4. Feedback and exceptional states

| State | Customer sees | Behavior |
| --- | --- | --- |
| Empty cart | Your order is empty. Tap a product to begin. | Total 0.00; checkout unavailable |
| Item added/changed | Short item-specific confirmation; visible quantity/total | Feedback does not steal keyboard focus |
| Invalid quantity | Clear explanation near affected row | No negative/fractional quantity; no silent cart corruption |
| Remove / decrease to zero | Item disappears with feedback | Zero removes the line; explicit Remove remains available |
| Cash blank/invalid | Enter a valid amount in pesos, with up to two decimal places. | Stay on payment; preserve editable input; no sale |
| Cash insufficient | Insufficient payment. Total is 240.00; you are short by 40.00. | Stay on payment; no successful reference/receipt |
| Cash exact/excess | Change preview 0.00 / correct positive amount | Server still validates on Pay now |
| Processing | Processing simulated card payment... | Disable repeated action, announce state; server result determines success |
| Server/storage error | Payment could not be completed. Please try again. | No success claim or partially stored sale; retry uses the same attempt |
| Catalog changed after review | Your order changed. Please review the updated amount. | Return to review; invalidate the old payment attempt |
| Expired cart/session | Your session has ended. Please start a new order. | Return to empty selection; never infer payment success |
| Unauthorized/stale receipt link | Receipt unavailable for this transaction. | Do not reveal another customer's sale; offer return to selection |
| Focus | Clearly outlined current control | Keyboard path works; no focus hidden by sticky bar |
| Success | Payment successful with actual transaction details | Receipt becomes available only after the completed sale is stored |

Cash keypad: digits, decimal separator, backspace, and Clear. Limit to two fractional digits with useful feedback rather than silently rounding entered payment. No quick-denomination buttons are required. JavaScript improves entry, but normal form submission and server validation remain authoritative.

## 5. Proposed storage and record responsibilities

SQLite is the accepted storage direction for the local exam demonstration: it is already configured, needs no separate database service, and supports persistent catalog/sale records. Persistent storage is our chosen approach, not a mandatory database requirement from the exam. Django's database-backed anonymous session stores the active cart separately from the completed-sale records.

| Record | Proposed fields / responsibility |
| --- | --- |
| Product | Stable seed key, display name, two-decimal price, selectable flag; no stock quantity |
| Transaction | Internal ID; database-unique public reference; database-unique payment-attempt UUID; customer-context UUID; completion timestamp; method; total; amount paid; change |
| TransactionItem | Transaction link; product identifier when available; snapshotted product name, unit price, positive integer quantity, subtotal |
| Session kiosk namespace | Cart as product-ID/quantity pairs; cart revision; active customer-context UUID; current reviewed-order fingerprint; current payment-attempt UUID/method; active completed transaction ID |

Session values must be JSON-serializable: IDs, integers, strings, and dictionaries. Do not store Python Decimal objects in JSON sessions; derive totals from product data or use canonical decimal strings for reviewed facts. Reassign the cart/session namespace after updates so changes are saved reliably.

Snapshots preserve exactly what was bought and paid even if the catalog changes later. Historical items must survive removal/deactivation of a product; do not cascade-delete sale items through a product relationship. Receipt rendering reads stored transaction/item values, not the current mutable cart or catalog.

### Money and trusted calculations

- Compute with Python Decimal from decimal strings/validated database values, never binary float arithmetic. Display exactly two decimals.
- Unit price and quantity come from validated server/catalog state. Browser-submitted prices, subtotals, change, and totals are not trusted.
- Subtotal = unit price x positive integer quantity; total = sum of subtotals; cash change = amount paid - total. No tax/discount additions are proposed.
- Reject blank, invalid, negative, non-finite, out-of-field-range, and insufficient cash amounts. Proposed input policy rejects more than two decimal places rather than silently rounding. Match maximum values to the actual model fields during implementation.
- Product prices must be positive. An empty cart cannot produce a sale. QR/card amount paid is assigned from the trusted total, with zero change.
- Model money fields use two decimal places. SQLite has limitations for database decimal arithmetic; calculate monetary results in Python and test exact stored/displayed values. No SQL floating-point total computation. Reassess the backend if deployment requirements become materially different.

### Review consistency and references

On Continue from review, calculate a server fingerprint from product IDs, names/prices, quantities, and cart revision. A new attempt UUID represents that reviewed order. If quantities or catalog facts change, invalidate that attempt and require review again before payment. Payment-method changes before completion may keep the order attempt but update the validated method; stale method forms are rejected.

Proposed display reference: `CT-` followed by a generated UUID encoded without separators, displayed with sensible line wrapping. Enforce uniqueness in the database and retry generation on a genuine reference collision; do not rely solely on a sample counter or date. A shorter display format can be chosen in implementation only with an adequate uniqueness policy. The public reference is not an access credential.

## 6. Allowed state transitions

| Current state | Allowed next state | Guard / retained data |
| --- | --- | --- |
| Selecting | Reviewing | Nonempty validated cart; retain selections |
| Reviewing | Selecting | Back keeps cart; editing invalidates old payment facts |
| Reviewing | Choosing payment | Validate current products/quantities and reviewed fingerprint |
| Choosing payment | Cash / QR / Card ready | Valid reviewed cart and supported method |
| Cash / QR / Card ready | Choosing payment | Change method; order remains, stale amount/form feedback cleared |
| Choosing payment | Reviewing | Back retains cart; further editing invalidates attempt |
| Cash ready | Cash ready on failure / Completed on success | Cash validated; invalid payment creates no sale |
| QR ready | Completed | Explicit simulated confirmation; server validates current order |
| Card ready | Processing -> Completed | Explicit process action; brief visible status, then validated server completion |
| Processing | Ready with error on failed request | No New Transaction/Back mutation while the completion request is in flight; retry safely |
| Completed | Receipt | Only the active completed transaction for this session/context |
| Receipt | Selecting with a new customer context | Explicit New Transaction resets active state |

All mutations use POST with CSRF protection; page GETs do not complete a sale or reset state. Use Post/Redirect/Get for successful mutations. Direct links cannot skip guards. After completion, old cart/payment pages resolve to the active completion/receipt rather than reopening the paid order. Invalid/incomplete payments cannot access successful receipts.

The Card Processing state is a customer feedback state, not a new database sale status or real bank authorization. Backend completion is the same trusted operation used by cash and QR.

### Duplicate completion policy

Disabling the button is helpful but insufficient. A unique payment-attempt UUID stored on Transaction is the backend duplicate guard. In one database atomic operation, validate the attempt/context/order, create the sale and all snapshotted item rows, or roll back all of them on failure. A repeated submission for an already completed attempt returns that same sale only when it is still the session's authorized active transaction; it never creates another receipt reference or changes its paid amount/method.

Use database uniqueness plus a handled conflict path that fetches the existing authorized sale after rollback. SQLite does not provide effective `select_for_update` row locking; do not design around that assumption. Treat a database-busy failure as a failed request with retry, not as success. Exact failure/conflict handling is to be designed and tested during implementation.

Concurrent multi-tab reset/payment is outside the supported normal single-customer kiosk interaction. Prevent navigation while a payment request is in flight, reject stale attempts, and test repeat submission, stale forms, and ordinary Back/reload. Do not claim full multi-terminal concurrency guarantees for this simple local design.

## 7. Reset and consecutive-customer isolation

New Transaction is a POST action from the receipt. Clear the active cart, revision/reviewed facts, selected method, cash entry/error state, attempt UUID, and active transaction ID. Start a new customer-context UUID and rotate the session identifier; keep unrelated application session values only if needed. The completed database transaction/items are retained as history, with no public history screen.

Success/receipt access must match both the active transaction ID and current session customer context. A URL containing an earlier reference or ID cannot restore access after reset. A different browser/session cannot read that sale. Payment/receipt responses should not be cached, and history restoration must revalidate current state before redisplaying private transaction details; handle browser back/forward cache behavior where applicable. Ordinary Back, reload, and direct URLs after reset are explicit verification cases, not guarantees established by this document.

No previous-customer details go in localStorage or permanent client-side cart/receipt caches. After reset, selection shows an empty cart, total 0.00, and brief New transaction started feedback. A future application with accounts or multiple terminals would need a reviewed session/lifecycle policy beyond this baseline.

## 8. Decisions to review before implementation

| Decision | Proposal | Status |
| --- | --- | --- |
| Identity | Common Table; Campus bites and everyday favorites | Direction accepted 2026-10-07 |
| Palette/layout | Common Table colors; latest menu beside desktop order panel | Earlier full-width plan accepted; latest layout requested by Magos, rendered acceptance pending |
| Catalog | Six items and prices in section 2 | Direction accepted 2026-10-07 |
| Storage | SQLite catalog/completed sales; database-backed session cart | Direction accepted 2026-10-07 |
| Money policy | Decimal; two decimals; reject excess fractional digits | Supporting design specification; implementation verification pending |
| Completion | Shared atomic operation; unique reference and attempt | Supporting design specification; implementation verification pending |
| Reset | Clear active state, rotate context/session access; retain historical rows | Supporting design specification; implementation verification pending |

Acceptance was explicitly supplied by the user and recorded in EXAM_PLAN.md. This approves the planning direction; it does not verify the interface or data behavior, assign member work, or invoke Prompt 03. Setup/evidence work can begin when Prompt 03 is requested; later stages remain separate.

## 9. Sources, verification, and next stage

This document maps F01-F20 to screens and behavior; `docs/EXAM_PLAN.md` retains the full assignment/checklist mapping. Colors were checked computationally; layout, keyboard use, and all runtime/data behavior remain unimplemented and unverified. Do not mark functional checklist items passed from this proposal.

Official references supporting technical and accessibility facts (our design recommendations are separate):
- [Django anonymous/database-backed sessions](https://docs.djangoproject.com/en/6.1/topics/http/sessions/)
- [Django atomic database operations](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)
- [Django SQLite limitations](https://docs.djangoproject.com/en/6.1/ref/databases/#sqlite-notes)
- [Tailwind local CSS build](https://tailwindcss.com/docs/installation/tailwind-cli)
- [WCAG text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [WCAG target-size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

Next: Prompt 03 (setup and evidence records) when requested. Magos's identity and today's 21:00 Asia/Singapore deadline are recorded. Individual GitHub accounts and any separate professor instructions still need to be supplied. Keep required functionality and genuine evidence first; optional enhancements remain excluded.


## 10. Prompt 04 implementation checkpoint

2026-10-07: the accepted Common Table direction now has a locally verified base page. Earlier sections preserve the design proposal at its original planning stage; data and transaction behaviors remain unimplemented. This checkpoint does not approve extra features or alter the accepted catalog.

Implemented: system sans typography (18px body), cream canvas, green brand/hero, plum details, restrained borders, generous spacing, menu area above the full-width order area, our own static line artwork, 48px minimum controls, 56px review/disclosure, visible 3px CSS focus outline and reduced-motion CSS. The progress include supports Choose/Review/Pay/Receipt; none is active on this pre-order foundation. Empty/unavailable menu and order copy is explicit. Review is disabled, not connected to pretend checkout. The native disclosure works without JavaScript. Reusable error/success/info/loading feedback uses escaped text, alert/status roles and loading aria-busy; no transaction outcomes are invented.

Desktop (1280×900), tablet (768×1024) and narrow (360×800) browser previews showed no horizontal overflow. Keyboard skip link moved focus to main; the disclosure opened using Enter and had a visible outline. Computed body text was 18px; all current control heights were at least 48px. Text contrast checks passed for the used palette; detailed ratios are in TEST_RESULTS.md. Actual touchscreen hardware, screen-reader operation, 200% zoom, OS reduced-motion toggling, and the future transaction screens were not tested. Original SVGs are code assets, not professor-sample artwork.

[Foundation screenshot](evidence/ui-foundation-desktop.jpg). Built stylesheet: kiosk/static/kiosk/css/app.css; editable source: kiosk/assets/input.css. All runtime assets are local. Prompt 05 is next after the scoped Git checkpoint and feature branch preparation; it implements the accepted data foundation rather than changing the design silently.


## 11. Modern foundation revision — pending visual acceptance

Requested by Magos after seeing the first Prompt 04 page. The user wants modern appeal without excessive styling and wants to review the design before progressing. The revision was implemented within the existing UI branch/milestone and checked locally on 2026-10-07. This is a requested design iteration, not a fabricated refactoring or bug-fix stage.

- Original Common Table identity now uses a lowercase, tightly spaced wordmark and a custom CT symbol. No online font, logo asset, professor sample asset or frontend framework was added.
- Cooler light canvas `#F7F8F5`; dark forest hero `#163F34`; restrained lime accent `#D5EDAA`. Existing leaf, ink, muted, plum and error colors remain available. This updates the original warm-canvas proposal in response to user feedback; new colors are our design choices, not exam requirements.
- Hero title is 52px at wide desktop, 44px tablet and 36px narrow screens, with compact line spacing. Other reading text stays 16–18px; this is an intentional refinement of the earlier smaller headline proposal.
- Original vector rice bowl, toast and drink artwork adds character without a remote image/CDN dependency. It is decorative, uses empty alt and aria-hidden, and is not a product card or selectable catalog. Desktop/tablet uses two hero columns; narrow screens place the illustration below the text.
- Content max-width 1120px. Menu area remains above the full-width order area. Menu-unavailable status is a compact horizontal card on wider screens, stacked on narrow screens. Subtle shadows, layered order-card footer and restrained badges replace the large empty panels. There is still no active transaction and Review order is disabled.
- Informational progress remains a plain four-part line treatment. Real controls retain at least 48px height and visible focus; native ordering disclosure is keyboard-accessible. No decorative animation was added.

Verified: local CSS/art/favicon delivery, Django check, desktop/tablet/narrow no horizontal overflow, original illustration loaded, keyboard skip/disclosure and target heights. New text contrast: ink/canvas 12.27:1; muted/canvas 5.39:1; white/forest 11.70:1; lime/forest 9.21:1. These checks do not establish complete accessibility compliance. See TEST_RESULTS.md for pending physical touch, screen-reader and zoom checks.

[Revised desktop screenshot](evidence/ui-foundation-modern-desktop.jpg). [Earlier foundation screenshot](evidence/ui-foundation-desktop.jpg) remains historical evidence. User reaction to the revised rendered result is pending. Stay at design review rather than silently advancing to catalog/data implementation.


## 12. UI milestone submitted for the Git review checkpoint

After the revised preview, Magos stated the current milestone was completed and checked and explicitly requested commit/push/PR creation. The revised visual foundation is therefore the scope being recorded for review. This later request supersedes the earlier wait-before-Git state, but does not invent a detailed human design evaluation, instructor acceptance or independent code review. The design remains original and transaction requirements remain future work.

## 13. Current menu-and-order workspace - visual review pending

Magos explicitly requested adapting the sample UI's organization while keeping our own theme/project. The sample was visually rechecked: its selection screen places a product grid beside an order panel with a visible total/action area. The current local revision adopts that familiar pattern, not its navy/orange theme, branding, assets or exact screen reproduction. This overrides the earlier products-above-order layout; colors and data architecture remain our own. It is a design iteration within Prompt 04, not a new feature or fabricated bug-fix/refactor stage.

- Compact white Common Table header, CT symbol, calm green/light canvas, system typography and plain four-step progress. The large welcome hero is removed.
- Content max-width 1320px. At 1024px and above, flexible menu plus a 340px sticky order panel. Product grid is three columns at 1280px and above, two at 420-1279px, and one below 420px. Below 1024px, order panel follows products in normal flow. One vertical page scroll; no nested order scroll in this preview.
- Six cards show the agreed names and two-decimal PHP prices, short descriptions and original inline food SVG artwork. No sample artwork or external font/image/CDN is used.
- Right panel provides an explicit empty order, 0 items, static zero total and disabled Review order. Every product card is also genuinely disabled and labeled unavailable. These fixtures do not satisfy product selection, quantity controls or trusted calculation requirements; later stages bind server product/cart data.
- Typography: 28/32px page heading, 18px product names, 16px descriptions, 20px prices. Existing touch controls, focus, escaped feedback and reduced-motion styling remain.
- Future review, payment choices, cash/QR/card, success, receipt and reset retain the state/validation design in earlier sections. They will use the same visual language and clear totals/actions; no new payment screens or state behavior were implemented here.

Local Tailwind build, Django check, root rendering, valid inline artwork references, desktop/tablet/narrow overflow and keyboard skip/disclosure checks passed. Full accessibility and application acceptance remain pending. See TEST_RESULTS.md for observed sizes and limits.

[Current workspace screenshot](evidence/ui-foundation-workspace-desktop.jpg). User satisfaction/acceptance is pending. Local branch codex/ui-foundation at fa76162 plus uncommitted changes; PR #2 still contains the earlier hero design. No Git mutations were performed. Review this result before the scoped Git checkpoint and reusable E/Prompt 05.

### Later checkout observation

The next reusable E request found the workspace revision already committed as 3cad483 and clean; this supersedes section 13's earlier uncommitted-state snapshot. Magos requested proceeding to the next feature branch, which is prepared as codex/catalog-data from that commit. This supports advancing with the current layout; detailed personal visual evaluation, instructor approval and peer review are not inferred. No design or application code changed during branch preparation.

## 14. Prompt 05 data decisions implemented

SQLite product, completed Transaction and TransactionItem tables now exist. DATA.md documents every field. Unit prices use eight total digits/two decimals; sale/subtotal/paid/change use ten/two. Product price, line subtotal and sale total must be positive; quantity range is 1-99 per line. These limits and optional product descriptions are implementation choices, not professor rules. Session/customer behavior and original workspace design are unchanged.

Stable seed keys create only missing products; existing catalog edits are intentionally preserved. Historical lines retain name/unit-price/quantity/subtotal snapshots when products are edited/deleted. Database uniqueness protects public references and payment-attempt UUIDs. Python clean/full_clean enforces exact Decimal cash-change and line arithmetic; database checks enforce supported methods/ranges and exact QR/card values. Future shared completion must call full_clean, validate aggregate totals/nonempty orders and save all records atomically. No database-enforced immutable history, payment endpoint, session authorization or reset implementation is claimed.

All 14 data tests passed; local migrate/seed/reseed and migration-drift checks passed. See TEST_RESULTS.md. Magos requested simplifying future branch names; catalog-data is the actual local feature branch based on UI evidence commit 3ce83e2. Later authorized checkpoint recorded data code as a02288bca6d1fda50cfea7191066b25cf47e46e2 and [PR #3](https://github.com/Yray0-9/pos-app/pull/3); UI parent evidence is published. Genuine review pending; no cart work or merge. Stop before Prompt 06 implementation.
