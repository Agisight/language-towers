# Canonical language data

One language per BCP 47 folder. `meta.json` contains `id`, `name` and optional `order`.
Provider files are `<provider>.json`, with `schemaVersion`, `provider`,
`platformScores` (provisional category-level), `technologyScores` (granular),
and `evidence` (array of comment and URL entries per technology).

Do not create an `overall.json`: Overall is computed from provider data.
After editing run `python3 scripts/embed-data.py`.
