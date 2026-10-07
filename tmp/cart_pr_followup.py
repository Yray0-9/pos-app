import subprocess
from pathlib import Path
sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
path = Path('tmp/cart_pr_body.md')
path.write_text(path.read_text(encoding='utf-8-sig').rstrip() + f'\n\nDocumentation-only evidence follow-up: [{sha[:7]}](https://github.com/Yray0-9/pos-app/commit/{sha}). Records returned commit/branch/PR links, actual quota-only review state, configured responsibility and unresolved member/reviewer gaps. No application changes in this follow-up.\n', encoding='utf-8')
