import json
from pathlib import Path

result = json.loads(Path('tmp/cart_pr_status.json').read_text(encoding='utf-8'))
sha = result['head_sha']
url = result['url']
commit = f'https://github.com/Yray0-9/pos-app/commit/{sha}'
review = result['reviews'][0]['url'] if result['reviews'] else None
if result['head'] != 'cart-review' or result['base'] != 'catalog-data' or result['merged']:
    raise SystemExit('Unexpected PR state; evidence update aborted.')

summary = f'Prompt 06 selection/cart implementation [{sha[:7]}]({commit}) committed/pushed on cart-review; [PR #4]({url}) open/unmerged into catalog-data (base 796b5da). All 24 tests and configuration/dependency/migration/JavaScript/scope checks passed. Genuine review pending; quota-only bot COMMENTED notice, no inline/discussion findings or CI checks/statuses. Next numbered stage: Prompt 07 on the same cart-review branch after inspecting/reusing its state. No new branch, merge, deployment, reviewer contact or automatic feature work.'

def replace_prefix(file, prefix, replacement):
    path = Path(file)
    lines = path.read_text(encoding='utf-8').splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(f'{file}: expected exactly one prefix {prefix}')
    lines[matches[0]] = replacement
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

def append(file, body):
    path = Path(file)
    path.write_text(path.read_text(encoding='utf-8').rstrip() + '\n\n' + body.strip() + '\n', encoding='utf-8')

replace_prefix('README.md', '**Current milestone:**', '**Current milestone:** ' + summary + ' Review/payment/receipt/reset remain unimplemented; F07-F08 are pending.')
replace_prefix('README.md', 'Prompt 04 implementation:', 'Prompt 04 implementation: [6ff4a07](https://github.com/Yray0-9/pos-app/commit/6ff4a07cbc410b3436c6f6e2c4ed152fac33977b), on codex/ui-foundation. [UI PR #2](https://github.com/Yray0-9/pos-app/pull/2) targets codex/setup-foundation and remains unmerged. The cart checkpoint is now complete in PR #4. **Next numbered stage: Prompt 07, reusing cart-review after checking its actual state.**')
replace_prefix('docs/BUILD_PROMPTS.md', 'Current checkpoint:', 'Current checkpoint: ' + summary + ' Prior visual checks remain Prompt 06 evidence; no new browser/payment acceptance claimed. Main integration and genuine member work/explanations remain unresolved.')
replace_prefix('docs/BUILD_PROMPTS.md', '**Current explicit delegation:**', '**Current explicit delegation:** The latest reusable B cart checkpoint has completed its scoped implementation commit/push and PR #4. Actual returned links/status are being recorded in a documentation-only follow-up under the same authorization. No blanket future Git actions, merge, deployment, reviewer messages or automatic Prompt 07. Keep the agreed simple cart-review branch for the next stage; configured author Romulo Magos remains unchanged.')
replace_prefix('docs/EXAM_PLAN.md', 'Current stage:', 'Current stage: ' + summary + ' F01/F03-F06 have local evidence, F02/F20 only selection-stage evidence. Individual Magos explanation, Agbas/Daro implementation/accounts, real peer review and main integration remain pending.')
replace_prefix('docs/MEMBER_REGISTER.md', '| Current local branch |', f'| Current local branch | cart-review, tracking origin/cart-review; implementation [{sha[:7]}]({commit}); [PR #4]({url}) open into catalog-data; genuine review pending |')

outcome = f'''## Cart B - actual publication and review outcome

2026-10-07, approximately 17:47-17:56 Asia/Singapore. Implementation commit [{sha}]({commit}), message Add touch-friendly selection and trusted session cart, configured author Romulo Magos, requester M3 Magos with Codex assistance. Exactly 21 scoped files; clean checkout observed after commit. Ordinary push created origin/cart-review/upstream; local/remote-tracking implementation SHAs matched. No force, merge, main change, branch creation, deployment or reviewer contact.

[PR #4]({url}) created and verified open/unmerged, publisher Yray0-9, source cart-review, target catalog-data at 796b5da. Diff against parent covers selection/cart and its relevant evidence, not repeated catalog implementation. Parent PR #3 remains open/unmerged; earlier setup/UI parents also unmerged. Main private-file/history/application issue remains separate and unresolved.

Actual feedback source: [Copilot quota notice]({review}), COMMENTED; bot explicitly could not review. No inline findings, discussion comments, requested code changes, CI checks/statuses or approval. No invented feedback/resolution. Genuine non-author review needed from Agbas/Daro after confirming accounts or an instructor-accepted reviewer. Magos's independent understanding and Agbas/Daro implementation/contribution evidence remain pending. The configured name change is preserved as observed; no identity/configuration was changed by the assistant.

This documentation-only follow-up records the real returned commit/PR/review evidence under the current checkpoint authorization; it is evidence maintenance, not an artificial new application development stage. Next numbered stage Prompt 07 reuses cart-review after inspection. No automatic feature implementation.
'''
for file in ('docs/AI_LOG.md', 'docs/MEMBER_REGISTER.md', 'docs/EXAM_PLAN.md'):
    append(file, outcome)
append('docs/TEST_RESULTS.md', f'''## Cart B - actual commit/push/PR verification

Scoped stage/whitespace/current-private-secret review passed for 21 files. Commit {sha} created by configured author Romulo Magos; clean checkout after commit. Ordinary git push -u origin cart-review succeeded; local HEAD and origin/cart-review matched. Diff against origin/catalog-data is 21 milestone/evidence files. env/database/cache/tmp excluded.

PR #4 {url}: open/unmerged, head cart-review at implementation SHA, base catalog-data 796b5da, publisher Yray0-9. Review inspection returned quota-only Copilot COMMENTED notice, no inline/discussion findings, no check runs/statuses. No human approval, CI success, merge or review resolution claimed. Parent PRs remain open. Current checkpoint validation is 24 tests plus configuration/dependency/migration/Node/whitespace/scope checks; previous visual/CSS checks not rerun unnecessarily. Documentation-only follow-up adds actual results; final publish/head/clean-state check follows its commit.
''')
append('README.md', f'''## Selection/cart Git checkpoint

Implementation [{sha[:7]}]({commit}) is pushed on [cart-review](https://github.com/Yray0-9/pos-app/tree/cart-review), with [PR #4]({url}) open into catalog-data. Configured author Romulo Magos retained; authenticated publisher Yray0-9. Actual evidence is in MEMBER_REGISTER.md and TEST_RESULTS.md. A documentation-only follow-up records returned links/status.

The [bot quota comment]({review}) is not approval. A genuine non-author reviewer (Agbas/Daro with confirmed account, or an instructor-accepted reviewer) must inspect the diff, verify the stated behavior and provide actual feedback. No reviewer contacted and no merge. Other member feature contributions and individual explanations remain pending. Next: Prompt 07 on the same branch after state inspection; no new branch is necessary merely because the prompt number changes.
''')
append('docs/DATA.md', f'Prompt 06 calculation/session implementation is now recorded as [{sha[:7]}]({commit}) on cart-review and [PR #4]({url}) into catalog-data. No storage/schema changes at the Git checkpoint; review/payment completion/reset work remains pending.')
append('docs/DESIGN.md', f'Later Git checkpoint: live selection design is in implementation [{sha[:7]}]({commit}), published on cart-review with [PR #4]({url}) open into catalog-data. Screenshot remains actual Prompt 06 evidence; no new visual acceptance or independent review is inferred from publication.')
