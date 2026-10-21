#!/usr/bin/env python3
"""Validate submitted language assessments, without merging or changing canonical scores."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / 'data' / 'categories.json'
PLATFORMS = ROOT / 'data' / 'config.json'
CONTRIB = ROOT / 'contributions'
LANGUAGE_TAG = re.compile(r'^[a-z]{2,8}(?:-[a-z0-9]{2,8})*$', re.I)


def check(path, technology_ids, providers):
    errors = []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return [f'{path}: unreadable JSON: {exc}']
    if not isinstance(data, dict):
        return [f'{path}: top-level must be an object']
    language = data.get('language')
    if not isinstance(language, dict):
        errors.append('language must be an object')
        language = {}
    lang_id = language.get('id')
    if not isinstance(lang_id, str) or not LANGUAGE_TAG.fullmatch(lang_id):
        errors.append('language.id must be a BCP 47-style tag, e.g. tyv or zh-Hans')
    name = language.get('name')
    if not isinstance(name, dict) or not isinstance(name.get('en'), str) or not name['en'].strip():
        errors.append('language.name.en is required')
    provider = data.get('provider')
    if provider not in providers:
        errors.append(f'provider must be one of: {", ".join(sorted(providers))}')
    if provider == 'overall':
        errors.append('overall is computed and must not be submitted')
    if data.get('schemaVersion') != 1:
        errors.append('schemaVersion must be 1')
    scores = data.get('technologyScores')
    if not isinstance(scores, dict):
        errors.append('technologyScores must be an object')
        scores = {}
    if not scores:
        errors.append('technologyScores must include at least one assessment')
    for tid, score in scores.items():
        if tid not in technology_ids:
            errors.append(f'unknown technology: {tid}')
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100:
            errors.append(f'{tid}: score must be a number from 0 to 100')
    evidence = data.get('evidence', {})
    if not isinstance(evidence, dict):
        errors.append('evidence must be an object')
        evidence = {}
    for tid, items in evidence.items():
        if tid not in technology_ids:
            errors.append(f'unknown evidence technology: {tid}')
        if not isinstance(items, list):
            errors.append(f'{tid}: evidence must be an array')
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f'{tid}[{index}]: evidence entry must be an object')
                continue
            comment, url = item.get('comment'), item.get('url')
            if not isinstance(comment, str) or not isinstance(url, str):
                errors.append(f'{tid}[{index}]: comment and url must be strings')
            elif url:
                parsed = urlsplit(url)
                if parsed.scheme not in {'https', 'http'} or not parsed.netloc:
                    errors.append(f'{tid}[{index}]: invalid source URL: {url}')
    if isinstance(lang_id, str) and isinstance(provider, str) and path.name != f'{lang_id.lower()}-{provider}.json':
        errors.append(f'filename must be {lang_id.lower()}-{provider}.json')
    return [f'{path.relative_to(ROOT)}: {msg}' for msg in errors]


def main():
    groups = json.loads(SCHEMA.read_text(encoding='utf-8'))
    cfg = json.loads(PLATFORMS.read_text(encoding='utf-8'))
    technology_ids = {tech['id'] for group in groups for tech in group['technologies']}
    providers = {platform['id'] for platform in cfg['platforms'] if platform['id'] != 'overall'}
    files = sorted(CONTRIB.glob('*.json'))
    if not files:
        print('PASS: No contribution JSON files yet.')
        return 0
    errors = [problem for path in files for problem in check(path, technology_ids, providers)]
    if errors:
        for error in errors:
            print('ERROR:', error, file=sys.stderr)
        return 1
    print(f'PASS: Validated {len(files)} contribution JSON file(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
