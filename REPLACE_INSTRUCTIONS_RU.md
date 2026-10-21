# Переход на раздельные файлы языков

1. Распакуйте архив в отдельную папку.
2. В `~/Downloads/language-towers-or` сохраните `.git` (и собственный `.gitignore`).
3. Замените остальные файлы содержимым архива, включая скрытую `.github` и папку `lang`.
4. Выполните:

```bash
cd ~/Downloads/language-towers-or
python3 scripts/embed-data.py
python3 scripts/validate_contributions.py
node scripts/test_aggregation.js
git status
git add -A
git commit -m "Migrate language data to independent lang directories"
git push
```

Данные теперь редактируются в `lang/<язык>/<поставщик>.json`. Файлы в `data/` генерируются.
Не удаляйте `.git`! Старые значения и порядок языков сохранены.
