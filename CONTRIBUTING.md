# Contribute a Language / Добавить язык

Open [Create Your Language](contribute.html) (English default, Russian toggle). Enter the language code and names, select ONE provider, assess each technology, add any number of `(comment, URL)` entries, and download a JSON file.

## GitHub Pull Request (no command line needed)

1. Open https://github.com/Agisight/language-towers and click **Fork**.
2. Open your fork's `contributions/` folder → **Add file** → **Upload files**.
3. Upload your downloaded `<language>-<provider>.json`. Commit changes to a **new branch**.
4. Click **Contribute → Open pull request**; base repository should be `Agisight/language-towers`, branch `main`. Explain what you measured and cite evidence.
5. Submit and **wait for a maintainer's review**. Respond to comments, add references or revise estimates if requested. A submitted PR does not guarantee acceptance.

### JSON format

```json
{
  "schemaVersion": 1,
  "language": {"id": "tyv", "name": {"en": "Tuvan", "ru": "Тувинский"}},
  "provider": "apple",
  "technologyScores": {"layout": 100, "autocorrect": 0},
  "evidence": {
    "layout": [{"comment": "System keyboard available", "url": "https://example.org/source"}],
    "autocorrect": [{"comment": "Tested in iOS", "url": ""}]
  }
}
```

Each contribution concerns **one language + one provider**. A score of 0 means assessed absence, while omitted technologies are unknown. Overall / Cross-platform is *not* submitted; it is computed from providers.

## По-русски

Откройте `contribute.html`, заполните один язык и одну платформу, при необходимости добавьте несколько комментариев со ссылками для каждой технологии, скачайте JSON. Создайте **Fork**, загрузите JSON в папку `contributions/` своего форка, сделайте коммит в новую ветку и откройте **Pull Request** в `Agisight/language-towers:main`. Затем дождитесь проверки, отвечайте на комментарии и исправляйте данные при необходимости.

## Canonical data after review / Данные после проверки

The `contributions/` directory is for **proposals only**. Accepted provider data
is maintained in `lang/<language-code>/<provider>.json` alongside `meta.json`.
Maintainers can apply a reviewed proposal using:

```bash
python3 scripts/apply_contribution.py contributions/tyv-apple.json
python3 scripts/embed-data.py
python3 scripts/validate_contributions.py
```

Review the diff before merging; generated data files must be committed too.
`data/scores.json` and `data/languages.json` are generated compatibility outputs.
