# План изменения: Чтение выбранных полей задачи

Дата: 2026-10-02

Ветка: `codex/task-get-readback`
Ответственный: Codex

## 1. Цель

Сохранить старое чтение задачи и добавить чтение выбранных Planfix-полей через существующий `planfix_task_get`; завершить owner-authorized этап 1 clean E2E, merge PR и выпуском `0.1.2`.

## 2. Scope

Что входит:

1. Необязательный `fields: str | None` в схеме и существующем MCP tool; передача ненулевого значения в query GET `/task/{id}`.
2. Регрессионные проверки схемы, legacy-вызова без `fields`, передачи `fields` и сохранения обработки API-ошибок.
3. Один безопасный пример в README, запись в changelog, версия пакета `0.1.2` и ограничение MCP SDK до `<2` до миграции API.
4. Одна синтетическая live E2E task через текущий MCP STDIO server с readback выбранных полей, checklist/comment и закрытием задачи.
5. После полного E2E PASS и green CI — merge PR, release `0.1.2` и передача пользователю демокоманды; затем остановиться.

Что НЕ входит:

1. Новые MCP tools, orchestration, DataTag, employee lookup и несвязанные directory workflows.
2. Изменения приватного репозитория и этапы 2–4.

## 3. Изменяемые файлы/модули

1. `planfix_mcp/schemas/tasks.py`, `planfix_mcp/tools/tasks_core.py`, `planfix_mcp/client.py`.
2. `tests/test_client_http.py`, `tests/test_mcp_contract.py`.
3. `README.md`, `DOCS_ALIGNMENT.md`, `CHANGELOG.md`, `pyproject.toml`.

## 4. Риски

1. Не передавать query `fields`, если параметр не задан: некоторые ответы без него содержат только id.
2. Не менять текущие 58 имён tools и формат API-ошибок.
3. Live writes ограничены одной owner-authorized синтетической задачей; любые дополнительные сущности и UI deletion требуют отдельного подтверждения владельца.

## 5. План шагов

1. Добавить регрессии и подтвердить красный результат.
2. Добавить необязательный параметр через текущий schema -> tool -> client путь; добиться зелёных регрессий.
3. Обновить краткий пользовательский пример, changelog и версию пакета; перепроверить план и diff.
4. После review PASS: commit, локальный checkpoint, push feature branch, draft PR и один короткий CI snapshot.
5. При CI fail по несовместимости MCP SDK: проверить clean-install log и официальный migration guide; ограничить SDK до `<2`, затем повторить локальные тесты/build и проверить новый CI run.
6. Завершить одну owner-authorized E2E задачу с точным readback и штатным закрытием.
7. После clean E2E и green CI обновить PR/план, merge, выпустить `0.1.2`, передать демокоманду и остановиться; новые задачи не создавать.

## 6. Критерии готовности

1. Без `fields` запрос остаётся `GET /task/{id}` без query; с `fields` query передаётся без переупаковки.
2. Tool schema показывает optional string `fields`; ошибки клиента остаются прежними.
3. Регистрируется ровно 58 инструментов и сохраняется backward compatibility.
4. E2E readback подтверждает три уникальных пункта checklist, один комментарий и закрытую задачу.
5. CI green, PR merged, release `0.1.2` опубликован, пользователь получил демокоманду.

## 7. Проверки

1. Регрессии сначала падают, затем проходят; `python -m pytest -q`.
2. `python -m py_compile` для изменённых Python-файлов и `python scripts/smoke_tools.py`.
3. `python scripts/check_swagger_alignment.py`, `python -m pip check`, wheel build и `git diff --check`.

## 8. Checkpoint

После review PASS создан feature commit `8c0e79bacade8bab95f7b08b5464768d89be3273` и локальные refs `backup/20261002-1023-task-get-readback` / `checkpoint/20261002-1023-task-get-readback`. Backup refs остаются локальными; push разрешён только для `codex/task-get-readback`. На момент checkpoint merge/release ещё не выполнялись; текущая цель завершения указана выше.

## Фактический результат

1. До SDK-совместимости локально: `pytest`: 34 passed; `compileall`, `py_compile`, smoke 58/58, Swagger 1.7.7, wheel build `0.1.2` и `git diff --check` прошли.
2. `pip check` выявил несвязанную зависимость установленного окружения: `opentele 1.15.1 requires tgcrypto, which is not installed`; зависимости не менялись.
3. Независимый review: PASS, блокирующих замечаний нет; reviewer подтвердил 34 теста, smoke 58, Swagger 53 операции и успешную сборку.
4. В момент подготовки implementation PR live writes ещё не запускались; актуальный результат owner-approved stage 1 см. ниже.
5. Implementation commit: `8c0e79bacade8bab95f7b08b5464768d89be3273`; локальные backup refs созданы. Draft PR #1 опубликован: https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/pull/1. На момент исходной записи PR ещё не был merged.
6. CI run `36984100493` обнаружил, что clean install выбрал MCP SDK 2.x, где удалён `mcp.server.fastmcp`; тот же импорт используется сервером и тестом контракта. Локально установлен MCP SDK `1.26.0`, поэтому локальные тесты не выявили проблему.
7. Исправление ограничивает `mcp[cli]` диапазоном `>=1.12.0,<2`; API миграция не входит в этот этап. После ограничения прошли `pytest` (34 passed), tool smoke (58/58), Swagger alignment (53 operations, 1.7.7), wheel build (`0.1.2`) и staged `git diff --check`. Новый PR CI run запускается после push фикса.
8. GitHub `pip check` ранее отложен из-за несвязанного глобального конфликта `opentele 1.15.1` без `tgcrypto`; зависимости не менялись.

## Live E2E — stage 1 (2026-10-02)

Статус: `LIVE_E2E_PARTIAL`.

Проверка выполнялась через текущий MCP STDIO server. Readback подтвердил заголовок и трёхшаговое описание задачи, согласованного исполнителя, стандартный процесс, срок 17:00 в часовом поясе Europe/Belgrade и закрытие задачи штатным статусом. У template-based create первоначальный process readback отличался от стандартного процесса; тестовую запись выровняли существующим task-update tool и подтвердили отдельным readback.

Чеклист и комментарий проверялись отдельными list tools. Повторный проход по чеклисту использовал ответ без явного выбора полей, который не содержал названий, поэтому повторно добавил три пункта. После запроса `id,name,parent,isDone` подтверждено по две копии каждого пункта. Комментарий также был добавлен повторно; explicit-field readback выявил две копии, после удаления более поздней тестовой копии подтверждён ровно один активный комментарий.

В доступном публичном MCP contract нет операции удаления пункта чеклиста, поэтому дубликаты чеклиста остаются и требуют ручной очистки владельцем в UI. Результат сейчас — `LIVE_E2E_PARTIAL`, не PASS. После подтверждённой очистки до одного экземпляра каждого пункта, полного E2E PASS и green CI merge и release `0.1.2` входят в owner-authorized scope; отдельный повторный owner review PR не требуется. Подтверждение нужно только для UI login/deletion. После merge/release передать демокоманду и остановиться; новых задач не создавать. В публичный отчёт не включаются task ID, account URL или содержимое приватной конфигурации.
