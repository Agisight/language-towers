#!/usr/bin/env python3
"""Apply a reviewed contributions/<language>-<provider>.json to canonical lang/.
This is a maintainer action, not automatic PR acceptance.
Usage: python3 scripts/apply_contribution.py contributions/tyv-apple.json
"""
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_contributions import check


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 scripts/apply_contribution.py contributions/<lang>-<provider>.json')
    source = Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit(f'No such file: {source}')
    groups = json.loads((ROOT / 'data/categories.json').read_text())
    config = json.loads((ROOT / 'data/config.json').read_text())
    tids = {t['id'] for g in groups for t in g['technologies']}
    providers = {p['id'] for p in config['platforms'] if p['id'] != 'overall'}
    problems = check(source, tids, providers)
    if problems:
        raise SystemExit('\n'.join(problems))
    payload = json.loads(source.read_text(encoding='utf-8'))
    code, provider = payload['language']['id'], payload['provider']
    folder = ROOT / 'lang' / code
    folder.mkdir(parents=True, exist_ok=True)
    meta = folder / 'meta.json'
    if not meta.exists():
        meta.write_text(json.dumps({'id':code,'name':payload['language']['name']},ensure_ascii=False,indent=2)+'\n')
    target = folder / f'{provider}.json'
    current = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    # Preserve category fallback assessments and untouched technology scores.
    updated = {**current, 'schemaVersion':1, 'provider':provider}
    updated['platformScores'] = current.get('platformScores', {})
    updated['technologyScores'] = {**current.get('technologyScores', {}), **payload['technologyScores']}
    updated['evidence'] = {**current.get('evidence', {}), **payload.get('evidence', {})}
    target.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Applied reviewed contribution: {source.name} -> {target.relative_to(ROOT)}')
    print('Please review git diff, then run python3 scripts/embed-data.py')

if __name__ == '__main__':
    main()
