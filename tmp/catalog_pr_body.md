Adds the SQLite data foundation for Common Table: products, completed-sale headers and snapshotted sale items with two-decimal money, unique receipt references/payment-attempt UUIDs, payment-method/range checks and validated exact Python Decimal arithmetic. A repeatable seed command creates the six agreed products without duplicating IDs or overwriting existing edits. No cart, payment or receipt endpoints are added; the current screen remains a disabled preview.

Source: `catalog-data`. Target: `codex/ui-foundation`, the committed UI/setup dependency while parent PRs remain unmerged. Main currently needs separate application-history/private-file cleanup; this PR does not modify it. Requester: M3 Magos with Codex assistance; configured author Yray0-9. Agbas/Daro contributions and human explanations are not inferred.

Validation:
- 14 Django data tests passed: seed repeatability/preservation, Decimal roundtrip/arithmetic, unique references/attempts, payment/value checks, snapshots after product edits/deletion, protected history and atomic rollback.
- Django configuration and Python dependency checks passed; no migration drift or pending local migrations.
- Six local products validated; local sales/items remain zero. Existing root HTTP 200.
- Whitespace/scope/private-secret checks passed; local environment/database/package artifacts excluded.

Model save alone does not run full_clean. Aggregate totals, nonempty checkout, authorized duplicate HTTP payment handling, session isolation and immutable application behavior remain explicit future service-stage work; DATA.md records those boundaries. Actual non-author review is needed before merge. No peer approval is claimed and no reviewer was messaged.
