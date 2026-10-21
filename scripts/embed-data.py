#!/usr/bin/env python3
"""Build a self-contained offline HTML from separately editable JSON data files.

Source files:
  data/config.json, data/categories.json, data/languages.json, data/scores.json
Generated artifacts:
  data/language-data.json and index.html's embedded JSON payload.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
def read(filename):
    return json.loads((DATA / filename).read_text(encoding="utf-8"))

config = read("config.json")
groups = read("categories.json")
languages = read("languages.json")
scores = read("scores.json")

ids = [language["id"] for language in languages]
if len(set(ids)) != len(ids):
    raise SystemExit("Duplicate language ID in languages.json")
if len(set(g["id"] for g in groups)) != len(groups):
    raise SystemExit("Duplicate category ID in categories.json")
if set(scores) - set(ids):
    raise SystemExit("Scores contain unknown language IDs: " + ", ".join(sorted(set(scores) - set(ids))))

assembled = {**config, "groups": groups, "languages": []}
for language in languages:
    row = scores.get(language["id"], {})
    assembled["languages"].append({
        **language,
        "platformScores": row.get("platformScores", {}),
        "technologyScores": row.get("technologyScores", {}),
    })

render_data = json.dumps(assembled, ensure_ascii=False, indent=2)
(DATA / "language-data.json").write_text(render_data + "\n", encoding="utf-8")
html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
embedded = render_data.replace("</", "<" + "\\/")
updated, count = re.subn(
    r'(<script id="initial-data" type="application/json">)[\s\S]*?(</script>)',
    lambda match: match.group(1) + embedded + match.group(2),
    html,
    count=1,
)
if count != 1:
    raise SystemExit("Could not locate embedded data block in index.html")
html_path.write_text(updated, encoding="utf-8")
print(f"Built {len(languages)} languages × {len(groups)} categories; updated index.html")
