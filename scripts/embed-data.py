#!/usr/bin/env python3
"""Build Language Towers from independent lang/<code>/meta.json and provider JSON.

Canonical inputs: lang/, data/categories.json, data/config.json.
Generated compatibility files: data/languages.json, data/scores.json,
 data/language-data.json, plus embedded JSON in index.html.
Never edit generated files directly; edit files in lang/ instead.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
LANG = ROOT / 'lang'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def put(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    cfg = read(DATA / 'config.json')
    groups = read(DATA / 'categories.json')
    providers = {p['id'] for p in cfg['platforms'] if p['id'] != 'overall'}
    group_ids = {g['id'] for g in groups}
    technology_ids = {t['id'] for g in groups for t in g['technologies']}
    languages, scores = [], {}
    if not LANG.exists():
        raise SystemExit('Missing lang/ directory')
    for folder in LANG.iterdir():
        if not folder.is_dir():
            continue
        meta_path = folder / 'meta.json'
        if not meta_path.exists():
            raise SystemExit(f'Missing meta.json: {folder}')
        meta = read(meta_path)
        if meta.get('id') != folder.name:
            raise SystemExit(f'Language ID does not match folder: {folder}')
        name = meta.get('name')
        if not isinstance(name, dict) or not name.get('en'):
            raise SystemExit(f'Missing English name: {folder}')
        language = {'id': meta['id'], 'name': name}
        languages.append((meta.get('order', 1000000), language))
        entry = {'platformScores': {}, 'technologyScores': {}}
        for path in sorted(folder.glob('*.json')):
            if path.name == 'meta.json':
                continue
            provider = path.stem
            if provider not in providers:
                raise SystemExit(f'Unknown provider file: {path}')
            payload = read(path)
            if payload.get('provider', provider) != provider:
                raise SystemExit(f'Provider mismatch: {path}')
            categories = payload.get('platformScores', {})
            technologies = payload.get('technologyScores', {})
            if not isinstance(categories, dict) or not isinstance(technologies, dict):
                raise SystemExit(f'Invalid scores: {path}')
            for values, known, kind in [(categories, group_ids, 'category'), (technologies, technology_ids, 'technology')]:
                for k, v in values.items():
                    if k not in known:
                        raise SystemExit(f'Unknown {kind} {k}: {path}')
                    if v is not None and (isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 100):
                        raise SystemExit(f'Invalid score {k}: {path}')
            if categories:
                entry['platformScores'][provider] = categories
            if technologies:
                entry['technologyScores'][provider] = technologies
        scores[meta['id']] = entry
    languages = [lang for _, lang in sorted(languages, key=lambda x: (x[0], x[1]['id']))]
    if not languages:
        raise SystemExit('No languages in lang/')
    if len({item['id'] for item in languages}) != len(languages):
        raise SystemExit('Duplicate language IDs')
    combined = {**cfg, 'groups': groups, 'languages': []}
    for language in languages:
        row = scores[language['id']]
        combined['languages'].append({**language, **row})
    put(DATA / 'languages.json', languages)
    put(DATA / 'scores.json', scores)
    put(DATA / 'language-data.json', combined)
    render = json.dumps(combined, ensure_ascii=False, indent=2).replace('</', '<' + chr(92) + '/')
    target = ROOT / 'index.html'
    original = target.read_text(encoding='utf-8')
    html, count = re.subn(r'(<script id="initial-data" type="application/json">)[\s\S]*?(</script>)',
        lambda m: m.group(1) + render + m.group(2), original, count=1)
    if count != 1:
        raise SystemExit('Cannot find initial-data script in index.html')
    target.write_text(html, encoding='utf-8')
    print(f'Built {len(languages)} languages × {len(groups)} categories from lang/; updated index.html')

if __name__ == '__main__':
    main()
