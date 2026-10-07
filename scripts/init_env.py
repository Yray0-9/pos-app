"""Create a private development .env without replacing an existing file."""

import secrets
from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent.parent
    template = project_root / '.env.example'
    destination = project_root / '.env'
    contents = template.read_text(encoding='utf-8')
    placeholder = 'DJANGO_SECRET_KEY=\n'
    if contents.count(placeholder) != 1:
        raise SystemExit('The template must contain one blank DJANGO_SECRET_KEY entry.')
    contents = contents.replace(
        placeholder, f'DJANGO_SECRET_KEY={secrets.token_urlsafe(64)}\n', 1,
    )
    try:
        with destination.open('x', encoding='utf-8', newline='\n') as env_file:
            env_file.write(contents)
    except FileExistsError:
        print('Existing .env preserved; no values were displayed.')
    else:
        print('Created local .env; no values were displayed.')


if __name__ == '__main__':
    main()
