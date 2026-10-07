"""Scoped GitHub checkpoint helper; credentials stay in process memory."""

import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


REPO = 'Yray0-9/pos-app'
API = 'https://api.github.com'


def credential():
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    result = subprocess.run(
        ['git', 'credential', 'fill'],
        input='protocol=https\nhost=github.com\npath=Yray0-9/pos-app.git\n\n',
        text=True, capture_output=True, env=env,
    )
    if result.returncode:
        raise RuntimeError('Cached GitHub credentials are unavailable; no values displayed.')
    values = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    if not values.get('password'):
        raise RuntimeError('Cached GitHub credential is incomplete; no values displayed.')
    return values['password']


def request(path, method='GET', data=None, missing_ok=False):
    payload = json.dumps(data).encode() if data is not None else None
    req = Request(API + path, data=payload, method=method, headers={
        'Authorization': 'Bearer ' + credential(),
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/json',
        'User-Agent': 'Common-Table-exam-checkpoint',
    })
    try:
        with urlopen(req, timeout=25) as response:
            return json.load(response)
    except HTTPError as error:
        if missing_ok and error.code == 404:
            return None
        raise RuntimeError(f'GitHub request failed with HTTP {error.code}; credentials not displayed.') from None
    except URLError:
        raise RuntimeError('GitHub network request could not complete; credentials not displayed.') from None


def pr_record(pr):
    return {
        'number': pr['number'], 'url': pr['html_url'], 'state': pr['state'],
        'merged': pr.get('merged', False), 'author': pr['user']['login'],
        'head': pr['head']['ref'], 'head_sha': pr['head']['sha'],
        'base': pr['base']['ref'], 'base_sha': pr['base']['sha'],
    }


def inspect():
    user = request('/user')
    repo = request('/repos/' + REPO)
    refs = {}
    for branch in ('main', 'codex/setup-foundation', 'codex/ui-foundation', 'catalog-data', 'cart-review'):
        ref = request('/repos/' + REPO + '/git/ref/heads/' + quote(branch, safe=''), missing_ok=True)
        refs[branch] = ref['object']['sha'] if ref else None
    catalog = request('/repos/' + REPO + '/pulls?state=all&head=Yray0-9%3Acatalog-data&per_page=100')
    parents = []
    for number in (1, 2):
        pr = request(f'/repos/{REPO}/pulls/{number}')
        reviews = request(f'/repos/{REPO}/pulls/{number}/reviews?per_page=100')
        record = pr_record(pr)
        record['reviews'] = [{
            'author': r['user']['login'], 'state': r['state'], 'url': r['html_url'],
            'quota_message': 'quota' in r.get('body', '').lower() or 'limit' in r.get('body', '').lower(),
        } for r in reviews]
        parents.append(record)
    return {'account': user['login'], 'repo': repo['full_name'], 'private': repo['private'],
            'can_push': repo.get('permissions', {}).get('push'), 'refs': refs,
            'catalog_prs': [pr_record(pr) for pr in catalog], 'parent_prs': parents}


def publish_pr():
    body = Path('tmp/catalog_pr_body.md').read_text(encoding='utf-8')
    payload = {
        'title': 'Add catalog and completed-sale data foundation',
        'body': body, 'head': 'catalog-data', 'base': 'codex/ui-foundation',
    }
    existing = request('/repos/' + REPO + '/pulls?state=open&head=Yray0-9%3Acatalog-data&per_page=100')
    if len(existing) > 1:
        raise RuntimeError('Multiple open catalog PRs found; inspect before updating.')
    if existing:
        payload.pop('head')
        pr = request(f'/repos/{REPO}/pulls/{existing[0]["number"]}', 'PATCH', payload)
    else:
        pr = request('/repos/' + REPO + '/pulls', 'POST', payload)
    return pr_record(pr)


def status(number):
    pr = request(f'/repos/{REPO}/pulls/{number}')
    sha = pr['head']['sha']
    reviews = request(f'/repos/{REPO}/pulls/{number}/reviews?per_page=100')
    comments = request(f'/repos/{REPO}/pulls/{number}/comments?per_page=100')
    checks = request(f'/repos/{REPO}/commits/{sha}/check-runs')
    statuses = request(f'/repos/{REPO}/commits/{sha}/status')
    return dict(pr_record(pr), reviews=[{
        'author': r['user']['login'], 'state': r['state'], 'url': r['html_url'],
        'body': r.get('body', '')[:1500],
    } for r in reviews], inline_comments=[{
        'url': c['html_url'], 'path': c['path'], 'line': c['line'], 'body': c['body'][:1500],
    } for c in comments], checks=[{
        'name': c['name'], 'status': c['status'], 'conclusion': c['conclusion'],
    } for c in checks['check_runs']], statuses=[{
        'context': s['context'], 'state': s['state'],
    } for s in statuses['statuses']])


if __name__ == '__main__':
    try:
        action = sys.argv[1]
        result = inspect() if action == 'inspect' else publish_pr() if action == 'publish' else status(int(sys.argv[2]))
        print(json.dumps(result, indent=2))
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
