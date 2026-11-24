# Цифровой механик

Единый командный проект для конкурсной задачи «Цифровой механик».

## Назначение

Система связывает результаты внешней ML-диагностики с применимой технической документацией двигателя и помогает специалисту подготовить обоснованную заявку на ТОиР. Решение о ремонте и отправке заявки остаётся за человеком.

## Статус

**Подготовительный этап.** Репозиторий содержит проектную документацию и план работ. Конкурсная реализация начинается только после разрешённого организаторами старта: **26 ноября 2026, 10:00 (МСК)**.

До старта не размещать конкурсный код, рабочие промпты, конфигурации реализации или поисковые индексы, если это запрещено правилами конкурса. Если граница разрешённой подготовки неоднозначна, требуется письменное подтверждение организатора.

## Быстрый вход

1. Прочитать [QUICK_START](docs/QUICK_START.md) — порядок первых часов спринта.
2. Проверить [MISSING_INPUTS](docs/MISSING_INPUTS.md) — что необходимо получить и подтвердить.
3. Изучить [TASK_SPECIFICATIONS](docs/TASK_SPECIFICATIONS.md) — подробные инженерные постановки.
4. Открыть [GitHub Issues](https://github.com/DmitryKDI/DVS/issues) — очередь задач и критерии.
5. Свериться с [SPRINT_CONTROL](docs/SPRINT_CONTROL.md) — контрольные точки и управление очередью.

## OpenSpec

Для установки CLI из репозитория нужен Node.js 22.20.0 или новее.
В корне DVS выполните:

```sh
npm ci
npm run openspec -- --version
npm run openspec -- list
```

Версия CLI закреплена в `package-lock.json`. Конфигурация проекта хранится
в [openspec/config.yaml](openspec/config.yaml), а навыки Codex — в
[.agents/skills](.agents/skills). Повторно запускать `openspec init` после
клонирования не нужно.

Для новых задач Codex Cloud добавьте `npm ci` из корня DVS в скрипт настройки
среды. В задачах запускайте CLI через `npm run openspec -- <команда>`.

## RTK в Codex

Проектный навык [`rtk`](.agents/skills/rtk/SKILL.md) доступен в DVS.
Откройте репозиторий в Codex и вызовите `$rtk`. CLI устанавливается отдельно.
Для Linux выполните:

```sh
installer="$(mktemp)"
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/v1.2.1/install.sh -o "$installer" &&
  RTK_EDITION=oss RTK_VERSION=v1.2.1 sh "$installer"
rm -f "$installer"
export PATH="$HOME/.local/bin:$PATH"
rtk --version
rtk git status --short --branch
```

Для автоматического вызова в Codex CLI выполните `rtk init -g --codex` и
перезапустите процесс Codex CLI. В Codex Cloud можно вызывать `rtk` напрямую
после установки. [Официальные инструкции RTK](https://github.com/rtk-ai/rtk).

## Локальная проверка диагностики

В корне DVS с Python 3.10 или новее выполните:

```sh
python3 -B -m dvs --local-test --scenario normal
python3 -B -m unittest discover -s tests -v
```

Доступны сценарии `normal`, `anomaly`, `poor-recording`, `unknown-status`
и `unavailable`. Тестовые результаты отмечены полем `synthetic: true`.
Без `--local-test` команда сообщает о недоступности источника до подключения
реального ML.

## Локальный сквозной каркас

```sh
python3 -B -m dvs.local_workflow --scenario anomaly --submit-local
```

Команда показывает карточку синтетического автомобиля, диагностику, ссылку на
условный документ с цитатой и черновик. Пример сверяет модификацию
двигателя и цитату с синтетической страницей в памяти. Введите номер показанной версии для передачи
заявки в тестовый приёмник в памяти. Пример полностью локальный и не обращается
к ML, ТОиР или реальным PDF. Без `--submit-local` выводится только результат
проверки и черновик, если он доступен.

## Документация

- [Устав и границы проекта](docs/PROJECT_CHARTER.md)
- [Архитектура](docs/ARCHITECTURE.md)
- [Backlog](docs/BACKLOG.md)
- [Подробные постановки задач](docs/TASK_SPECIFICATIONS.md)
- [Матрица требований](docs/REQUIREMENTS.md)
- [Реестр недостающих данных](docs/MISSING_INPUTS.md)
- [План быстрого старта](docs/QUICK_START.md)
- [Управление спринтом](docs/SPRINT_CONTROL.md)
- [Подключение участников](docs/TEAM_ONBOARDING.md)
- [Командный регламент](docs/TEAM_RULES.md)
- [План испытаний](docs/TEST_PLAN.md)
- [Реестр внешних API](docs/API_CONTRACTS.md)
- [Матрица применимости документов](docs/DOCUMENT_MAPPING.md)
- [Журнал архитектурных решений](docs/DECISIONS.md)
- [Известные ограничения и блокировки](docs/KNOWN_LIMITATIONS.md)

## Команда

- Руководитель проекта / системный интегратор — Дмитрий.
- Backend / ML Integration / RAG — участник A, назначить после подтверждения доступа.
- Frontend / QA — участник B, назначить после подтверждения доступа.
- Инструмент разработки — один общий Codex, работающий последовательно по утверждённым задачам.

## Правило качества

Задача считается выполненной только после проверки по критериям приёмки. Статусы задач: NOT STARTED / IN PROGRESS / BLOCKED / IN REVIEW / DONE. Результаты испытаний: PASS / FAIL / BLOCKED / NOT RUN. Не отмечать PASS без фактического подтверждения.
