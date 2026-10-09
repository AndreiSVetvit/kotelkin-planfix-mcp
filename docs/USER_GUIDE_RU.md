# Руководство Пользователя

Это руководство объясняет, как попробовать Kotelkin Planfix MCP как обычный пользователь.

## Что Это Такое

Kotelkin Planfix MCP - локальный MCP-сервер для Planfix. Он запускается на вашем компьютере, принимает tool calls от MCP-клиента через STDIO и обращается к Planfix REST API с вашим Planfix token.

Это не публичный web-сервис. Токен не хранится в репозитории.
Требования: Python 3.12+ и аккаунт Planfix с доступом к REST API.

Руководство описывает версию пакета `v0.1.3`, основанную на опубликованном baseline [`v0.1.2`](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases/tag/v0.1.2). Актуальный опубликованный tag см. на странице [Releases](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases).

## Что Можно Делать

После настройки MCP-клиента можно просить примерно такие действия:

- "Создай в Planfix задачу `Подготовить счет`."
- "Покажи задачу 12345 из Planfix."
- "Перенеси срок задачи на завтра 11:00."
- "Добавь комментарий к задаче 12345."
- "Создай пункт чеклиста в задаче 12345."
- "Покажи шаблоны проектов Planfix."
- "Покажи записи справочника 10."
- "Получи статусы процесса задач."

Точная формулировка зависит от MCP-клиента. Сервер предоставляет инструменты, а клиент решает, как их показывать пользователю.

## Установка Из Исходников

Склонируйте репозиторий и создайте виртуальное окружение:

```bash
git clone https://github.com/AndreiSVetvit/kotelkin-planfix-mcp.git
cd kotelkin-planfix-mcp
python -m venv .venv
```

Установка без активации окружения. В PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

В macOS/Linux:

```bash
.venv/bin/python -m pip install -e .
```

Для разработки и тестов:

```bash
python -m pip install -e ".[dev]"
```

В PowerShell без активации используйте ` .\.venv\Scripts\python.exe -m pip install -e ".[dev]" `.

## Настройка Planfix Credentials

Минимальный вариант - переменные окружения:

```bash
PLANFIX_BASE_URL=https://your-company.planfix.com/rest
PLANFIX_TOKEN=your_token_here
```

Или можно сохранить credentials в OS keyring:

```bash
planfix-mcp-secrets-init
```

Команда запросит token без отображения ввода и сохранит оба значения в OS keyring.
В PowerShell без активации используйте ` .\.venv\Scripts\planfix-mcp-secrets-init.exe `; в macOS/Linux — `.venv/bin/planfix-mcp-secrets-init`.

Не добавляйте токены в Git, issue, screenshots и публичные логи.

## Настройка MCP-Клиента

Подключите сервер как STDIO MCP command:

Для Codex CLI укажите абсолютный путь к executable из `.venv`, чтобы запуск не зависел от активированного shell:

```bash
# PowerShell
codex mcp add kotelkin-planfix-mcp -- (Resolve-Path .venv\Scripts\planfix-mcp-server.exe).Path
# macOS/Linux
codex mcp add kotelkin-planfix-mcp -- "$(pwd)/.venv/bin/planfix-mcp-server"
codex mcp list
```

Проверьте подключение через `/mcp` в Codex. Это локальный STDIO-сервер, не hosted endpoint.

```json
{
  "mcpServers": {
    "kotelkin-planfix-mcp": {
      "command": "planfix-mcp-server",
      "env": {
        "PLANFIX_BASE_URL": "https://your-company.planfix.com/rest",
        "PLANFIX_TOKEN": "your_token_here"
      }
    }
  }
}
```

Если клиент умеет наследовать локальные переменные окружения, блок `env` можно не дублировать после локальной настройки.

## Безопасная Первая Проверка

Проверить регистрацию инструментов без обращения к Planfix:

```bash
planfix-mcp-smoke
```

В PowerShell без активации используйте ` .\.venv\Scripts\planfix-mcp-smoke.exe `; в macOS/Linux — `.venv/bin/planfix-mcp-smoke`.

Проверить реальный токен:

```bash
planfix-mcp-preflight
```

По умолчанию preflight выполняет только read-only `GET /ping` и `GET /workspace/list`. Список задач не запрашивается, если явно не задан `PLANFIX_PREFLIGHT_TASK_LIST=1`. В PowerShell без активации используйте ` .\.venv\Scripts\planfix-mcp-preflight.exe `; в macOS/Linux — `.venv/bin/planfix-mcp-preflight`.

Для безопасного первого запроса к Codex попросите вызвать `planfix_task_get` с `task_id` уже известной задачи и `fields="id,name,status,endDateTime"`. В ответе нужно сообщить только эти четыре поля. При первой проверке не просите создавать или менять записи.

Если нужно проверить и список задач:

```bash
PLANFIX_PREFLIGHT_TASK_LIST=1 planfix-mcp-preflight
```

## Live QA На Тестовом Аккаунте

Используйте тестовый Planfix-аккаунт или рабочее пространство, где не страшно создать тестовые записи.

Базовая live-проверка:

```bash
planfix-mcp-live-qa-basic
```

Если процесс задачи запрещает комментарии, передайте id существующей задачи, где комментарии разрешены:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 planfix-mcp-live-qa-basic
```

Расширенная live-проверка:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 \
PLANFIX_LIVE_QA_DATATAG_ID=10 \
PLANFIX_LIVE_QA_ASSIGNEE_ID=1 \
PLANFIX_LIVE_QA_DIRECTORY_ID=10 \
planfix-mcp-live-qa-extended
```

Постоянные изменения конфигурации аккаунта, например создание custom fields, по умолчанию выключены. Включайте только на тестовом аккаунте:

```bash
PLANFIX_LIVE_QA_CONFIG_WRITES=1 planfix-mcp-live-qa-extended
```

## Группы Инструментов

Сервер регистрирует 58 инструментов:

- Задачи: создание, получение, обновление, список, сроки, статусы, исполнители, файлы, шаблоны, регулярные задачи, фильтры.
- Комментарии: список, добавление, обновление, получение, удаление.
- Чеклисты: создание, список, получение пункта, обновление пункта.
- DataTags: добавление в задачу и к существующему комментарию.
- Проекты: создание, список, группы, шаблоны, получение, обновление, файлы.
- Справочники: группы, список, получение, записи, фильтры.
- Процессы и объекты: списки и статусы.
- Кастомные поля: группы, списки, создание, получение.

Точные примеры входных данных: [MANUAL_QA_EXTENDED_TOOLS.md](../MANUAL_QA_EXTENDED_TOOLS.md).

## Важное По Безопасности

Инструменты чтения обычно низкорисковые. Инструменты записи меняют данные в Planfix.

Перед подключением к production Planfix:

- создайте токен только с нужными scopes;
- сначала проверьте на тестовом аккаунте;
- оставьте консервативный `PLANFIX_MIN_REQUEST_INTERVAL_SEC`;
- проверьте, какие процессы задач разрешают комментарии, статусы и назначение исполнителей;
- не коммитьте MCP config с реальным токеном.

## Частые Проблемы

Ошибка авторизации обычно значит, что токен не сохранен, истек или у него нет нужного scope.

Business validation error обычно значит, что выбранный процесс Planfix запрещает операцию. Например, некоторые процессы запрещают новые комментарии.

Если `planfix_task_get_statuses` не может определить статусы из задачи, передайте `process_id` или `object_id`:

```json
{
  "task_id": 12345,
  "payload": {
    "process_id": 100206
  }
}
```
