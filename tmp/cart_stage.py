import subprocess
from dotenv import dotenv_values

files = ['README.md', 'docs/AI_LOG.md', 'docs/BUILD_PROMPTS.md', 'docs/DATA.md',
         'docs/DESIGN.md', 'docs/EXAM_PLAN.md', 'docs/MEMBER_REGISTER.md', 'docs/TEST_RESULTS.md',
         'docs/evidence/cart-desktop.jpg', 'kiosk/assets/input.css', 'kiosk/cart.py',
         'kiosk/static/kiosk/css/app.css', 'kiosk/static/kiosk/js/cart.js',
         'kiosk/templates/kiosk/base.html', 'kiosk/templates/kiosk/home.html',
         'kiosk/templates/kiosk/components/product_preview.html',
         'kiosk/templates/kiosk/components/product_card.html',
         'kiosk/templates/kiosk/components/workspace.html',
         'kiosk/test_cart.py', 'kiosk/urls.py', 'kiosk/views.py']
if subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() != 'cart-review':
    raise SystemExit('Checkout changed; stage aborted.')
if subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).strip():
    raise SystemExit('Pre-existing staged changes; stage aborted.')
subprocess.run(['git', 'add', '--', *files], check=True)
staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
if set(staged) != set(files):
    raise SystemExit('Staged scope differs; inspect before commit.')
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
secret = dotenv_values('.env').get('DJANGO_SECRET_KEY')
for name in staged:
    result = subprocess.run(['git', 'show', ':' + name], capture_output=True)
    if result.returncode == 0 and secret and secret.encode() in result.stdout:
        raise SystemExit('Private value found; commit blocked, values withheld.')
print('Scoped stage, whitespace and private-secret review passed:', len(staged), 'files')
subprocess.run(['git', 'diff', '--cached', '--stat'], check=True)
