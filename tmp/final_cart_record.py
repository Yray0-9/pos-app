from pathlib import Path
path = Path('README.md')
text = path.read_text(encoding='utf-8')
text = text.replace('The browser demo currently contains two rice bowls, one wrap and one lemonade (PHP 279.50).', 'The saved screenshot captures two rice bowls, one wrap and one lemonade (PHP 279.50); the live cart can change through further interaction.')
path.write_text(text, encoding='utf-8')
path = Path('docs/TEST_RESULTS.md')
text = path.read_text(encoding='utf-8')
text = text.replace('Final demo order rice x2/wrap/lemonade, 4 units, 279.50.', 'Screenshot order rice x2/wrap/lemonade, 4 units, 279.50. Later browser reload observed rice x3/wrap/lemonade x2, 6 units, 404.00; the shared live order had changed after capture and was preserved without attributing the interaction to a member.')
text += '\nFinal recheck: all 24 tests passed again in 0.924s; Django configuration, dependency/migration drift, node --check cart.js and git diff --check passed. Local branch/HEAD unchanged (cart-review/796b5da); feature screenshot/code are not ignored, temporary documentation helper is ignored. Final browser reload preserved the later 404.00 order and Review remained disabled.\n'
path.write_text(text, encoding='utf-8')
