from pathlib import Path
from urllib.parse import urlsplit
import subprocess
from dotenv import dotenv_values

expected = 'https://github.com/Yray0-9/pos-app.git'
for flag in ([], ['--push']):
    value = subprocess.check_output(['git', 'remote', 'get-url', *flag, 'origin'], text=True).strip()
    parsed = urlsplit(value)
    if value != expected or parsed.username or parsed.password:
        raise SystemExit('Remote does not exactly match the confirmed intended URL; values withheld.')
print('Origin fetch/push verified:', expected)
changes = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
new = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()
secret = dotenv_values('.env').get('DJANGO_SECRET_KEY')
for name in changes + new:
    path = Path(name)
    if path.is_file() and secret and secret.encode() in path.read_bytes():
        raise SystemExit('Private value found in milestone content; values withheld.')
print('Private secret absent from changed/new shareable files. Files:', len(changes + new))
for path in (Path('AGENTS.md'), Path('../AGENTS.md'), Path('../../AGENTS.md')):
    if path.is_file():
        print(path, path.read_text(encoding='utf-8'))
