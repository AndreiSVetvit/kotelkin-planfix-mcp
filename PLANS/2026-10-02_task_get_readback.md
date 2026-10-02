# План изменения: Чтение выбранных полей задачи

Дата: 2026-10-02

Ветка: `codex/task-get-readback`
Ответственный: Codex

## 1. Цель

Сохранить старое чтение задачи и добавить чтение выбранных Planfix-полей через существующий `planfix_task_get`.

## 2. Scope

Что входит:

1. Необязательный `fields: str | None` в схеме и существующем MCP tool; передача ненулевого значения в query GET `/task/{id}`.
2. Регрессионные проверки схемы, legacy-вызова без `fields`, передачи `fields` и сохранения обработки API-ошибок.
3. Один безопасный пример в README, запись в changelog и версия пакета `0.1.2`.

Что НЕ входит:

1. Новые MCP tools, orchestration, live QA writes, DataTag или employee lookup.
2. Изменения приватного репозитория и unrelated QA runner; merge, release и live writes.

## 3. Изменяемые файлы/модули

1. `planfix_mcp/schemas/tasks.py`, `planfix_mcp/tools/tasks_core.py`, `planfix_mcp/client.py`.
2. `tests/test_client_http.py`, `tests/test_mcp_contract.py`.
3. `README.md`, `DOCS_ALIGNMENT.md`, `CHANGELOG.md`, `pyproject.toml`.

## 4. Риски

1. Не передавать query `fields`, если параметр не задан: некоторые ответы без него содержат только id.
2. Не менять текущие 58 имён tools и формат API-ошибок.
3. Не выполнять live writes без отдельной safe-конфигурации и approval gate.

## 5. План шагов

1. Добавить регрессии и подтвердить красный результат.
2. Добавить необязательный параметр через текущий schema -> tool -> client путь; добиться зелёных регрессий.
3. Обновить краткий пользовательский пример, changelog и версию пакета; перепроверить план и diff.
4. После review PASS: commit, локальный checkpoint, push feature branch, draft PR и один короткий CI snapshot.

## 6. Критерии готовности

1. Без `fields` запрос остаётся `GET /task/{id}` без query; с `fields` query передаётся без переупаковки.
2. Tool schema показывает optional string `fields`; ошибки клиента остаются прежними.
3. Регистрируется ровно 58 инструментов; draft PR опубликован, live QA writes не выполнялись.

## 7. Проверки

1. Регрессии сначала падают, затем проходят; `python -m pytest -q`.
2. `python -m py_compile` для изменённых Python-файлов и `python scripts/smoke_tools.py`.
3. `python scripts/check_swagger_alignment.py`, `python -m pip check`, wheel build и `git diff --check`.

## 8. Checkpoint

После review PASS создан feature commit `8c0e79bacade8bab95f7b08b5464768d89be3273` и локальные refs `backup/20261002-1023-task-get-readback` / `checkpoint/20261002-1023-task-get-readback`. Backup refs остаются локальными; push разрешён только для `codex/task-get-readback`. Не merge и не release.

## Фактический результат

1. `pytest`: 34 passed; `compileall`, `py_compile`, smoke 58/58, Swagger 1.7.7, wheel build `0.1.2` и `git diff --check` прошли.
2. `pip check` выявил несвязанную зависимость установленного окружения: `opentele 1.15.1 requires tgcrypto, which is not installed`; зависимости не менялись.
3. Независимый review: PASS, блокирующих замечаний нет; reviewer подтвердил 34 теста, smoke 58, Swagger 53 операции и успешную сборку.
4. `LIVE_E2E_NOT_RUN`: writes не запускались; ждём отдельный owner-approved безопасный аккаунт/workspace и точные значения теста.
5. Implementation commit: `8c0e79bacade8bab95f7b08b5464768d89be3273`; draft PR metadata будет добавлена после публикации. Merge и release вне этого этапа.
