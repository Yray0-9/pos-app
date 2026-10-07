The previously disabled catalog now supports adding products and editing a persistent current order. Selecting the same product combines its quantity; decrease at one removes the line, and Remove deletes it explicitly. All subtotals and totals use current SQLite prices and Python Decimal, ignoring submitted browser money.

Source: cart-review. Target: catalog-data at 796b5da. Catalog PR #3 remains open/unmerged into codex/ui-foundation; this base keeps the review scoped to selection/cart and its evidence. Implementation commit: f901b32620a3a53c298664f945813bf34f34cf28.

Implemented six database-backed cards, strict IDs and 1-99 quantities, session persistence/context/revision, POST/CSRF actions, disclosed stale-cart repair, maximum-total validation, touch controls and a modest server-rendered JavaScript enhancement with native form fallback. Review stays disabled until Prompt 07; no payment, receipt or reset is implemented. Existing branch-preparation evidence is included.

Validation:
- 24 Django tests pass (14 data plus 10 cart scenarios), including repeated selection, quantity/removal/zero rules, exact arithmetic, session isolation, malformed/stale state, untrusted browser prices, limits and CSRF/native fallback.
- Django check, pip check, migration drift check, existing Node runtime syntax check and staged whitespace/private-secret/scope review passed at this checkpoint. Local database remains six products, zero completed sales/items.
- Prior Prompt 06 local Tailwind build and browser checks passed: PHP 279.50/364.50/240.00 scenario, reload persistence, keyboard focus, controls >=48 CSS pixels, and no horizontal overflow at 1280x900, 768x1024 and 360x800. These browser checks were not rerun during the Git checkpoint. Saved screenshot: docs/evidence/cart-desktop.jpg.
- Browser debugging found and fixed input name action shadowing form.action; full interaction passed after using getAttribute('action'). See docs/AI_LOG.md and TEST_RESULTS.md for actual evidence and limitations.

Responsibility: requested by M3 Magos, implementation/checks with Codex assistance; configured commit author Romulo Magos and authenticated publisher Yray0-9. This does not establish Magos's independent explanation or any Agbas/Daro feature contribution. Genuine non-author review is needed from Agbas/Daro after account confirmation, or an instructor-accepted reviewer. No reviewer contacted or approval claimed. Prior parent PR comments are bot quota notices, not review approval.

Remaining: order review/back behavior (Prompt 07), simulated payments, receipt/reset and full exam/member verification. Physical touch, screen-reader testing and cross-tab concurrency are not guaranteed. Main integration/private-file history cleanup remains separate unresolved work; main was not modified. Do not merge automatically.

Documentation-only evidence follow-up: [11f7335](https://github.com/Yray0-9/pos-app/commit/11f7335f0311bb66e2de5f35a250dc09726af8fb). Records returned commit/branch/PR links, actual quota-only review state, configured responsibility and unresolved member/reviewer gaps. No application changes in this follow-up.
