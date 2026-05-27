# Чеклист Перед Публичной Публикацией

Этот чеклист нужен перед первым публичным GitHub-релизом Kotelkin Planfix MCP.

## Текущий Статус

Статус: `PARTIAL`.

MCP-продукт уже рабочий и прошел локальные и live-проверки. Но репозиторий лучше оставить private до финального утреннего review: имя, README, release notes, security notes и решение по открытию видимости.

## Что Увидят Люди После Открытия Репозитория

Пользователи GitHub увидят:

- исходный код MCP-сервера;
- README на английском и русском;
- user guides на английском и русском;
- MIT license;
- GitHub Actions CI;
- issue templates;
- security policy;
- manual QA examples и release checklist;
- package metadata и CLI entry points.

Они не увидят Planfix tokens, если токен случайно не будет закоммичен позже. Перед открытием нужно снова сделать secret scan.

## Как Пользователь Сможет Попробовать

1. Склонировать репозиторий.
2. Установить пакет:

```bash
python -m pip install -e .
```

3. Задать `PLANFIX_BASE_URL` и `PLANFIX_TOKEN`.
4. Проверить инструменты:

```bash
planfix-mcp-smoke
```

5. Проверить токен:

```bash
planfix-mcp-preflight
```

6. Добавить сервер в MCP-клиент:

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

## Что MCP Уже Умеет

- Работать с задачами Planfix.
- Менять сроки, статусы, исполнителей и custom fields.
- Работать с комментариями.
- Создавать и обновлять пункты чеклистов.
- Работать с DataTags.
- Работать с проектами.
- Читать и менять записи справочников.
- Читать процессы, объекты и статусы.
- Читать и создавать custom fields задач и проектов.

Всего сейчас регистрируется 58 инструментов MCP.

## Проверки Перед Открытием

Локально:

```bash
python -m pytest -q
python -m compileall planfix_mcp scripts tests
python scripts/smoke_tools.py
python scripts/check_swagger_alignment.py
python -m pip check
python -m pip wheel . --no-deps -w dist_tmp
```

На тестовом Planfix-аккаунте:

```bash
planfix-mcp-preflight
planfix-mcp-live-qa-basic
planfix-mcp-live-qa-extended
```

Secret scan:

```bash
rg --hidden --glob '!.git/**' --glob '!*.pyc' "PLANFIX_TOKEN|Authorization: Bearer|[0-9a-fA-F]{32}" .
```

Все совпадения нужно просмотреть глазами. Placeholder в `.env.example` допустим, реальный токен недопустим.

## Минимальная Планка Для Public v0.1.0

- Репозиторий остается private до финального review.
- Default branch чистый.
- GitHub CI проходит.
- README простым языком объясняет пользу.
- Есть русская документация.
- Нет приватного локального операционного слоя: panel, bridge, tracker, control-plane state, private Planfix task links, local runbooks, SQL.
- Нет реального токена, приватных путей и локального рабочего состояния.
- MCP tool names не меняются без отдельного contract proposal.
- Live QA прошел на тестовом Planfix-аккаунте или в рабочем пространстве, где допустимы тестовые записи.

## Рекомендуемая Форма Первого Релиза

- Tag: `v0.1.0`
- Release title: `Kotelkin Planfix MCP v0.1.0`
- Видимость: public только после финального maintainer review.
- GitHub description: `MCP server for Planfix REST API over STDIO`
- Topics: `mcp`, `model-context-protocol`, `planfix`, `planfix-api`, `python`

## Что Не Делать Перед v0.1.0

- Не переносить tracker, bridge, project panel, local control layer, local state, SQL и private runbooks.
- Не переименовывать public tool names без contract change proposal.
- Не публиковать tokens и screenshots с tokens.
- Не заявлять production-ready: текущий статус Alpha.
- Не добавлять hosted/cloud layer.

## Утренний Следующий Шаг

Открыть локально `README.md`, `README_EN.md`, `docs/USER_GUIDE.md`, `docs/USER_GUIDE_RU.md` и прочитать их глазами нового пользователя. Если путь понятен, следующий шаг - финальный maintainer review и подготовка `v0.1.0` release/tag.
