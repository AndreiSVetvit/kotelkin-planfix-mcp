# Kotelkin Planfix MCP

[Русский](README.md) | [English](README_EN.md)

MCP-сервер для работы с Planfix REST API.

Проект подключает Planfix к MCP-клиентам через STDIO transport. После настройки токена MCP-клиент может создавать и читать задачи, обновлять сроки и статусы, работать с комментариями, чеклистами, проектами, справочниками, процессами, объектами, кастомными полями и DataTags.

Текущая версия готовится как первый публичный кандидат `v0.1.0`: ядро отделено от локальных приватных операционных слоев, в репозитории нет bridge/panel/tracker/control-plane материалов.

## Что Это Даёт

- Один MCP-сервер для Planfix.
- 58 MCP tools поверх Planfix REST API.
- Запуск через STDIO, без отдельного web-сервера.
- Авторизация через Planfix bearer token.
- Локальные проверки без вызова Planfix.
- Live QA через настоящий MCP STDIO-сервер на тестовом Planfix-аккаунте.

## Кому Это Полезно

- Пользователям Planfix, которые хотят подключить свой аккаунт к MCP-клиенту.
- Разработчикам, которым нужен небольшой и понятный Planfix MCP server.
- Тем, кто хочет автоматизировать задачи, комментарии, чеклисты, проекты и справочники Planfix через AI-инструменты.

## Требования

- Python 3.12+
- Аккаунт Planfix с доступом к REST API
- `PLANFIX_BASE_URL`, например `https://your-company.planfix.com/rest`
- `PLANFIX_TOKEN`

Официальные источники Planfix REST API:

- https://planfix.com/ru/help/REST_API
- https://help.planfix.com/restapidocs/
- https://help.planfix.com/restapidocs/swagger.json

## Установка

```bash
python -m pip install -e .
```

Для разработки и тестов:

```bash
python -m pip install -e ".[dev]"
```

## Настройка

Минимальные переменные окружения:

```bash
PLANFIX_BASE_URL=https://your-company.planfix.com/rest
PLANFIX_TOKEN=your_token_here
```

Дополнительные настройки:

```bash
PLANFIX_TIMEOUT_SEC=20
PLANFIX_RETRY_MAX=2
PLANFIX_MIN_REQUEST_INTERVAL_SEC=1.0
PLANFIX_STATUS_CHANGE_DELAY_SEC=1.0
PLANFIX_SILENT_DEFAULT=false
LOG_LEVEL=INFO
```

Токен нельзя коммитить в репозиторий. Для локального использования можно сохранить токен в OS keyring:

```bash
planfix-mcp-secrets-init
```

## Запуск

```bash
planfix-mcp-server
```

Или:

```bash
python -m planfix_mcp.server
```

## Конфигурация MCP-Клиента

Пример формы конфигурации:

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

## Быстрая Проверка

Проверка регистрации tools без вызова Planfix:

```bash
planfix-mcp-smoke
```

Проверка соответствия официальному Swagger Planfix:

```bash
planfix-mcp-swagger-check
```

Проверка реальных credentials:

```bash
planfix-mcp-preflight
```

Базовая live-проверка через MCP STDIO:

```bash
planfix-mcp-live-qa-basic
```

Расширенная live-проверка на тестовом аккаунте:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 \
PLANFIX_LIVE_QA_DATATAG_ID=10 \
PLANFIX_LIVE_QA_ASSIGNEE_ID=1 \
PLANFIX_LIVE_QA_DIRECTORY_ID=10 \
planfix-mcp-live-qa-extended
```

Постоянные изменения конфигурации Planfix, например создание custom fields, включаются только отдельным флагом:

```bash
PLANFIX_LIVE_QA_CONFIG_WRITES=1 planfix-mcp-live-qa-extended
```

## Что Умеет MCP

- Задачи: создать, получить, обновить, найти списком.
- Сроки, статусы, исполнители и кастомные поля задач.
- Комментарии: список, добавление, обновление, получение, удаление.
- Чеклисты: создание, список, получение пункта, обновление.
- DataTags: добавление в задачу и к существующему комментарию.
- Проекты: создание, список, группы, шаблоны, получение, обновление, файлы.
- Справочники: группы, список, получение, записи, фильтры.
- Процессы и объекты: списки и статусы.
- Кастомные поля задач и проектов.

Полный список tools и payload-примеры: [MANUAL_QA_EXTENDED_TOOLS.md](MANUAL_QA_EXTENDED_TOOLS.md).

## Безопасность

Некоторые tools пишут в Planfix. Для проверки используйте тестовый аккаунт или low-risk workspace.

Токены храните в переменных окружения, OS keyring или настройках MCP-клиента вне Git. Не добавляйте токены в README, issue, логи или screenshots.

## Документация

- [User Guide](docs/USER_GUIDE.md)
- [Руководство пользователя](docs/USER_GUIDE_RU.md)
- [Public Release Checklist](docs/PUBLIC_RELEASE_CHECKLIST.md)
- [Чеклист перед публикацией](docs/PUBLIC_RELEASE_CHECKLIST_RU.md)
- [Planfix REST Docs Alignment](DOCS_ALIGNMENT.md)

## Статус

Статус: private public-candidate staging.

Код уже работает как MCP-продукт, но публичное открытие репозитория должно быть отдельным maintainer-решением после финального review имени, README, security notes и release notes.

## Лицензия

MIT
