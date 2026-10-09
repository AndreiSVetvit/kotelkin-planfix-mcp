# План изменения: Чистый публичный старт v0.1.3

Дата: 2026-10-09
Ветка: `codex/issue-3-clean-start`
Ответственный: Codex

## Результат

Новый пользователь видит baseline `v0.1.2`, устанавливает сервер, проходит локальный smoke, подключает STDIO к Codex и начинает с чтения существующей задачи. Демо не меняет данные Planfix.

## Scope

- Убрать preparing `v0.1.0` / private staging; дать ссылки на baseline и GitHub Releases.
- Согласовать короткий RU/EN clone -> install -> smoke/preflight -> Codex путь, guides, release checklists и roadmap Q4 2026.
- Подготовить metadata/changelog patch `0.1.3`; сохранить 58-tool contract.
- Не реализовывать NEXT #4/#5, новые tools, plugin/skill, hosted MCP или live QA writes.

## Файлы

`README.md`, `README_EN.md`, `README_RU.md`, `docs/USER_GUIDE.md`, `docs/USER_GUIDE_RU.md`, оба `docs/PUBLIC_RELEASE_CHECKLIST*`, `ROADMAP.md`, `CHANGELOG.md`, `pyproject.toml`, эта запись в `PLANS/`.

## Чеклист

- [ ] Обновить RU/EN baseline, Codex setup и безопасный read-only первый сценарий; сверить CLI syntax с `codex mcp --help`.
- [ ] Уточнить в Q4 roadmap: #4 local Codex pilot; #5 read-only overview только после реального использования #4 и решения владельца.
- [ ] Поставить версию `0.1.3` и записать release notes; публикация после maintainer review и зелёного CI.
- [ ] Проверить из новой venv:

```powershell
$venv = Join-Path $env:TEMP ("kotelkin-planfix-mcp-issue3-" + [guid]::NewGuid())
python -m venv $venv
& "$venv\Scripts\python.exe" -m pip install -e ".[dev]"
& "$venv\Scripts\python.exe" -m pytest -q
& "$venv\Scripts\python.exe" -m compileall planfix_mcp scripts tests
& "$venv\Scripts\python.exe" scripts/smoke_tools.py
& "$venv\Scripts\python.exe" scripts/check_swagger_alignment.py
& "$venv\Scripts\python.exe" -m pip check
& "$venv\Scripts\python.exe" -m pip wheel . --no-deps -w (Join-Path $venv "wheels")
git diff --check
```

- [ ] Preflight только по существующему keyring и только read-only; не запускать live QA.
