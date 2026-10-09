# Чеклист Публичного Релиза

Этот чеклист для maintenance-релиза `v0.1.3`, основанного на опубликованном baseline [`v0.1.2`](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases/tag/v0.1.2). Текущий опубликованный tag см. в [Releases](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases). До merge и публикации необходимы maintainer review и зелёный GitHub CI.

## Локальные проверки

На чистом checkout с Python 3.12+ создайте изолированное окружение и установите dev extra из инструкции проекта:

```powershell
python -m venv .venv
$testPython = ".\.venv\Scripts\python.exe"
& $testPython -m pip install -e ".[dev]"
& $testPython -m pytest -q
& $testPython -m compileall planfix_mcp scripts tests
& $testPython scripts/smoke_tools.py
& $testPython scripts/check_swagger_alignment.py
& $testPython -m pip check
& $testPython -m pip wheel . --no-deps -w dist_tmp
git diff --check
```

В macOS/Linux:

```bash
python -m venv .venv
PYTHON=.venv/bin/python
"$PYTHON" -m pip install -e ".[dev]"
"$PYTHON" -m pytest -q
"$PYTHON" -m compileall planfix_mcp scripts tests
"$PYTHON" scripts/smoke_tools.py
"$PYTHON" scripts/check_swagger_alignment.py
"$PYTHON" -m pip check
"$PYTHON" -m pip wheel . --no-deps -w dist_tmp
git diff --check
```

Swagger check требует сеть. Smoke должен подтвердить регистрацию 58 инструментов и не обращается к Planfix. С уже настроенными credentials можно отдельно выполнить `planfix-mcp-preflight`; по умолчанию это только `GET /ping` и `GET /workspace/list`. Live QA не входит в docs-only scope `v0.1.3`; будущий live run требует явно выбранного тестового аккаунта или low-risk workspace, поскольку runners записывают тестовые данные.

В Windows без активации окружения запускайте optional preflight через ` .\.venv\Scripts\planfix-mcp-preflight.exe `; в macOS/Linux — `.venv/bin/planfix-mcp-preflight`.

## Перед публикацией

- [ ] README, руководства, roadmap и оба чеклиста согласованы относительно baseline `v0.1.2` и scope `v0.1.3`.
- [ ] Убедиться, что в коммит не попали приватные/локальные операционные файлы, состояние аккаунта, credentials или реальные tokens; проект остаётся Alpha, не production-ready.
- [ ] Вручную просмотреть все совпадения secret scan; в tracked-файлах допустимы только placeholders:

```bash
rg --hidden --glob '!.git/**' --glob '!*.pyc' "PLANFIX_TOKEN|Authorization: Bearer|[0-9a-fA-F]{32}" .
```

- [ ] До merge пройти maintainer review и получить зелёный GitHub CI; публиковать `v0.1.3` только после одобренного merge.
- [ ] Сохранить контракт 58 инструментов и не запускать следующий `[NEXT]` issue автоматически.
