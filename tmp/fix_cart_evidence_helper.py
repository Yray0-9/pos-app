from pathlib import Path
path = Path('tmp/cart_after_publish.py')
text = path.read_text(encoding='utf-8-sig')
text = text.replace('({commit) on', '({commit}) on')
text = text.replace(".replace(f']({commit) ', f']({commit}) ')", '')
path.write_text(text, encoding='utf-8')
