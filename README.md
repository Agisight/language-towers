# Language Towers

**Open-source, data-driven visualization of digital language capabilities** across Apple, Android (AOSP), Google, Yandex, Microsoft, and independent community projects.

A language may have a technology on one platform but lack it on another. **Overall / Cross-platform is an automatic OR aggregation**, not a sixth vendor's manually invented scores.

- [Interactive towers](index.html) — editable SVG liquid-fill matrix; English default; Russian available.
- [Create Your Language](contribute.html) — submit one language/provider assessment with evidence and a live tower preview.
- [Contribution guidelines](CONTRIBUTING.md) — fork → JSON → Pull Request → review.
- [About & methodology](info.html) — bilingual explanation with examples of the OR calculation.
- [Canonical dataset](data/language-data.json) — assembled from the editable JSON files described above.

## Editing data independently (recommended)

Change JSON files in `data/` without editing HTML or JavaScript:

| File | Purpose |
| --- | --- |
| `data/languages.json` | Language IDs and translated display names; adding a language adds a column. |
| `data/categories.json` | Category order, descriptions, icons and nested technologies. |
| `data/scores.json` | Scores per language, platform and technology; `null` means not evaluated. |
| `data/config.json` | Site title, platform selection and bilingual metadata. |
| `data/language-data.json` | **Generated combined file** for compatibility; don't edit directly. |

After editing, run `python3 scripts/embed-data.py` (or `npm run build`). This rebuilds both the combined JSON and the standalone HTML; it requires only Python 3. You can then open `index.html` without a local server, and GitHub Pages can serve the exact same file.

**Editing in the browser is for experimentation only:** use Download JSON to export edits, then transfer the resulting changes into the appropriate source JSON files.

## How Overall works

For each **language and individual technology**, find the best evaluated implementation among Apple, Android AOSP, Google, Yandex, Microsoft and Independent / Community:

```text
Overall(language, technology) = MAX(known provider values)
Overall(language, category) = MEAN(known Overall technology values in the category)
```

If Apple supports technology A at 80% and Google supports technology B at 90%, both can contribute to the same Overall category. **Never simply MAX the vendors' aggregated category scores when detailed technology scores are available.**

### Missing values and provisional estimates

- `0` = an explicitly assessed absence of support.
- `null` / missing = **not evaluated** (not zero).
- If all sources are unknown, Overall is unknown.
- If only part of a category is evaluated, its displayed average covers only those known technologies and is marked as incomplete (`*`).
- Until any detailed technology values exist for a category, the older **group-level scores are retained**. Overall takes the maximum known group score as a **provisional fallback**. Such results also carry an incomplete marker if some sources are unassessed.
- A score is an estimate of availability, **not a scientific benchmark** or endorsement by a vendor.

## How to use

1. Open `index.html` directly in Safari or Chrome. No server, internet or build system required.
2. Choose a provider in **Platform**. The **Overall / Cross-platform** option is automatically calculated and is **read-only**.
3. Click a floor under a specific provider to edit its score. Click in Overall to inspect the computed estimate and known source(s).
4. Export the updated JSON with **Download JSON**, or upload a dataset to continue editing.
5. Open `info.html` for bilingual methodology. To open it in Russian directly, use `info.html?lang=ru`.

## Data model (v3)

```json
{
  "id": "tyv",
  "name": {"en": "Tuvan", "ru": "Тувинский"},
  "platformScores": {
    "apple": {"keyboard": 100, "keyboardTech": 0},
    "google": {"keyboard": null}
  },
  "technologyScores": {
    "google": {"machine": 75, "system": null},
    "community": {"machine": 65}
  }
}
```

`platformScores[providerId][groupId]` stores **legacy preliminary group estimates**. `technologyScores[providerId][technologyId]` is the intended, more precise model. Group definitions and technology IDs live in `groups[]` of the JSON dataset. **Do not write manually computed values under `platformScores.overall`.** The front end ignores any such value.

Add new languages to `languages[]` and providers to `platforms[]`; provider IDs must be unique. Adding a provider causes Overall to include its data automatically. Android (AOSP) and Google services are distinct; Community includes open-source and independent tools.

## Project structure

```text
index.html                    Offline interactive dashboard
info.html                     Bilingual explanation and methodology
assets/                       Reserved for future assets
data/language-data.json       Canonical JSON dataset
scripts/embed-data.py         Sync JSON into offline HTML
scripts/test_aggregation.js   Test OR / MAX logic without network
README.md                     This file
LICENSE                       MIT code license
DATA_LICENSE.md               Data and third-party rights policy
```

When changing canonical JSON, regenerate the embedded copy:

```bash
python3 scripts/embed-data.py
node scripts/test_aggregation.js
```

After that, commit both the four editable JSON files and regenerated `data/language-data.json` and `index.html`.

## Publish to GitHub Pages

1. Create repository `Agisight/language-towers` on GitHub.
2. Push the extracted files to `main`.
3. In **Settings → Pages**, choose **Deploy from a branch → `main` / `(root)`**.
4. Your site will be available at `https://agisight.github.io/language-towers/` when Pages finishes deploying.

No GitHub repository was created automatically by this export.

## Planned work

- Expandable per-technology floor details and provider-level evidence.
- Research provenance, dates, confidence levels and human review.
- More languages, custom comparisons, optional time-series history.
- Aggregation coverage indicators and weighting policies.

## License

Original application code: **MIT** (see `LICENSE`). Language corpora, third-party media and community datasets **are not automatically covered** (see `DATA_LICENSE.md`). This is an independent project, not affiliated with or endorsed by Apple, Google, Yandex or Microsoft.

---

## Кратко по-русски

Language Towers — независимый проект оценки цифровой поддержки языков. Режим **«Все платформы»** автоматически собирает лучший результат по каждой подтехнологии среди Apple, Android, Google, Яндекса, Microsoft и независимых решений (логическое **ИЛИ / максимум**). Затем подсчитывается среднее известных подтехнологий категории. Если пока есть только старые оценки целых категорий, временно берётся максимум известных оценок категории.

**`0` = подтверждённое отсутствие поддержки, `null` = не оценено.** Неизвестное никогда не превращаем в ноль; неполные оценки помечаются. Выберите конкретную платформу для правки данных, а общий режим остаётся вычисляемым и недоступным для ручного редактирования. Откройте `index.html` и `info.html` локально или разместите проект на GitHub Pages.


## Interface controls

The toolbar uses native accessible `<select>` elements with consistent SVG chevrons, explicit labels, and visible keyboard-focus styles. This affects appearance only; platform selection, localization, and data scores are unchanged.

## Print / PDF layout

Use **Print / PDF** in the top toolbar. The HTML automatically fits the entire
language matrix to a single **A3 landscape** page, including the last column.
Enable **Background graphics** in Chrome/Safari print settings so colored liquid
and glass fills are included. To output A4 instead, select A4 landscape and use
the print dialog's **Fit to page / Scale** setting, or keep A3 and export to PDF.

The language/platform controls use native accessible select elements with custom
chevron styling; their options and data logic are unchanged.

## Community contributions

Create your assessment in [Create Your Language](contribute.html), download a `<language>-<provider>.json`, upload it to the `contributions/` directory of your GitHub fork and open a Pull Request.

GitHub Actions runs `python3 scripts/validate_contributions.py` to validate the schema and source-link format. Structural validation does **not** verify factual scores. A maintainer reviews evidence and manually incorporates approved assessments into `data/scores.json`.

The editor and the main interface currently use distinct tank renderers; do not assume they are visually pixel-identical.
