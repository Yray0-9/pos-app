import json
import sys
from pathlib import Path
import catalog_checkpoint as github

REPO = github.REPO

def existing():
    return github.request(f'/repos/{REPO}/pulls?state=all&head=Yray0-9%3Acart-review&per_page=100')

def publish():
    prs = [pr for pr in existing() if pr['state'] == 'open']
    if len(prs) > 1:
        raise RuntimeError('Multiple open cart PRs; inspect before update.')
    payload = dict(title='Add touch-friendly selection and trusted session cart',
                   body=Path('tmp/cart_pr_body.md').read_text(encoding='utf-8'),
                   head='cart-review', base='catalog-data')
    if prs:
        if prs[0]['base']['ref'] != 'catalog-data':
            raise RuntimeError('Existing PR has a different base; inspect before update.')
        payload.pop('head')
        pr = github.request(f'/repos/{REPO}/pulls/{prs[0]["number"]}', 'PATCH', payload)
    else:
        pr = github.request(f'/repos/{REPO}/pulls', 'POST', payload)
    Path('tmp/cart_pr_result.json').write_text(json.dumps(github.pr_record(pr)), encoding='utf-8')
    return github.pr_record(pr)

if __name__ == '__main__':
    try:
        action = sys.argv[1]
        if action == 'inspect':
            result = [github.pr_record(pr) for pr in existing()]
        elif action == 'publish':
            result = publish()
        else:
            number = int(sys.argv[2])
            result = github.status(number)
            result['discussion_comments'] = [{
                'author': c['user']['login'], 'url': c['html_url'], 'body': c['body'][:1500]
            } for c in github.request(f'/repos/{REPO}/issues/{number}/comments?per_page=100')]
            Path('tmp/cart_pr_status.json').write_text(json.dumps(result), encoding='utf-8')
        print(json.dumps(result, indent=2))
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
