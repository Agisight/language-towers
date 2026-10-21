# Полная замена содержимого репозитория

1. Сохрани текущую папку как резервную копию (опционально).
2. В Finder, в корне `language-towers-or`, оставь папку `.git` и файл `.gitignore`. Удали остальные файлы и папки.
3. Скопируй **всё содержимое** этого архива в корень репозитория. Сохрани скрытую папку `.github` из архива — она содержит GitHub Actions. Не копируй папку `Language_Towers_COMPLETE_REPLACE` как вложенную папку.
4. Выполни из корня проекта:

```bash
python3 scripts/embed-data.py
python3 scripts/validate_contributions.py
node scripts/test_aggregation.js
git status
git add -A
git commit -m "Synchronize complete Language Towers project"
git push
```

`git add -A` требуется, чтобы включить созданные файлы, изменения и удаления.

**Осторожно:** не удаляй `.git` — в нём история и связь с GitHub. Если хочешь сохранить изменения, которых нет в архиве, сначала сделай резервную копию.

Проверяй `https://agisight.github.io/language-towers/` и `.../contribute.html` после публикации.
