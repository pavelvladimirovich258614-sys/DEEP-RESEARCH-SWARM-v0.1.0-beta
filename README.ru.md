# 🔎 DEEP RESEARCH SWARM

**Широкий поиск. Глубокая проверка. Один финал.**

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md)

> **Статус:** `v0.1.0-beta`
> Публичная бета-конфигурация для LobeHub — шесть специализированных агентов под управлением Куратора. Не облачный сервис. Не официальный продукт LobeHub.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Release: beta](https://img.shields.io/badge/Release-beta-orange.svg)
![LobeHub](https://img.shields.io/badge/%D0%94%D0%BB%D1%8F-LobeHub-1f6feb.svg)
![Multi-Agent](https://img.shields.io/badge/%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0-Multi--Agent-blueviolet.svg)
![Deep Research](https://img.shields.io/badge/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-Deep%20Research-2e7d32.svg)

---

## Зачем этот проект

Большинство «исследовательских агентов» втискивают разные задачи в один промпт: поиск, отбор источников, чтение, проверку, обработку противоречий и написание. DEEP RESEARCH SWARM разделяет эти задачи между специализированными агентами под управлением одного Куратора. Цель — **не** максимизировать число агентов, а построить дисциплинированный конвейер доказательств.

Система:

- параллельно ищет по сети, GitHub, форумам, научным статьям и официальной документации;
- предпочитает первоисточники пересказам;
- привязывает утверждения к источнику;
- различает факты, утверждения источника, сигналы сообщества и гипотезы;
- обнаруживает противоречия, а не сглаживает их;
- запускает таргетированную проверку там, где доказательств мало;
- возвращает **один связный ответ с реальными цитатами**.

## Архитектура

![Architecture](assets/architecture.svg)

```
User
  │
  ▼
Curator / Research Director (Supervisor)
  │
  ├──► Wide Web Scout
  │       обнаружение · fan-out запросов · candidate pool
  │
  ├──► Primary Source Hunter
  │       официальные доки · репозитории · статьи · релизы
  │
  ├──► Evidence Analyst
  │       глубокое чтение · Evidence Ledger · графы
  │
  ├──► Fact Checker / Red Team
  │       поиск противоречий · citation audit · блокирующий Quality Gate
  │
  └──► Research Synthesizer
          финальный синтез · неопределённость · цитаты · рекомендация
```

Это **звездообразная топология под управлением супервизора**. Специалисты возвращают работу Куратору и не делегируют друг другу рекурсивно.

## Шесть агентов

| Агент | Миссия | Типичный результат |
|---|---|---|
| **Curator / Research Director** | Планирует, маршрутизирует, контролирует глубину, объединяет доказательства, принимает финальное решение | план, workstreams, финальное решение |
| **Wide Web Scout** | Находит широкое поле кандидатов | ранжированный candidate pool + discovery map |
| **Primary Source Hunter** | Идёт за первоисточниками | provenance-first список URL |
| **Evidence Analyst** | Глубоко читает, извлекает пассажи, ведёт реестр | Evidence Ledger + Claim/Entity/Source графы |
| **Fact Checker / Red Team** | Пытается **опровергнуть** выводы, владеет блокирующим Quality Gate | PASS/FAIL со списком gaps |
| **Research Synthesizer** | Пишет единственный финальный ответ | одно Markdown-сообщение с цитатами на уровне утверждений |

Системные промпты — в `agents/`.

## Режимы исследования

Куратор масштабирует усилие под задачу. Можно зафиксировать режим явно.

| Режим | Когда | Открытые источники | Gap rounds |
|---|---|---|---|
| ⚡ QUICK | один факт / версия / цена | 3–8 | 0 |
| 🔹 STANDARD | «сравни X и Y» | 8–20 | 0–1 |
| 🔎 DEEP | «найди лучшие альтернативы» / решение | 20–50 | 1–2 |
| 🧠 MAX | «изучи рынок» / высокая цена ошибки | 30–80 | несколько |
| 🧬 ULTRA | только явный запрос «максимально глубоко» | 40–100 | max closure |

См. [`group/research-modes.md`](group/research-modes.md).

## Что вы получаете

- **Один финальный ответ** с цитатами на уровне утверждений; каждое утверждение ведёт к пассажу.
- **Настоящий Quality Gate.** Fact Checker пытается опровергнуть ответ до публикации. Если FAIL — цикл до закрытия критических gaps или до STOP RULE.
- **Evidence Ledger + графы.** У каждого утверждения есть происхождение: класс источника, дата, дата извлечения, confidence, verdict.
- **Глубина по режиму.** Простой вопрос → короткий ответ; рынок → 30+ источников.
- **Открытый код MIT.** Без вендор-лока.

## Быстрый старт

1. Прочитайте [`docs/lobehub-installation.md`](docs/lobehub-installation.md). Пошаговая настройка: создание группы, шесть агентов, вставка промптов, включение инструментов.
2. Запустите [`tests/acceptance-test.md`](tests/acceptance-test.md). Это валидирует конфигурацию до настоящего исследования.
3. Попробуйте [`examples/quick-research.md`](examples/quick-research.md) как первый прогон.
4. Попробуйте [`examples/deep-research.md`](examples/deep-research.md) для полного pipeline.

## Документация

- [`docs/architecture.md`](docs/architecture.md) — почему pipeline выглядит именно так
- [`docs/lobehub-installation.md`](docs/lobehub-installation.md) — пошаговая настройка
- [`docs/tools-and-skills.md`](docs/tools-and-skills.md) — что использует каждый агент
- [`docs/evidence-ledger.md`](docs/evidence-ledger.md) — схема, confidence, claim graph
- [`docs/citation-policy.md`](docs/citation-policy.md) — пятишаговая верификация
- [`docs/quality-gate.md`](docs/quality-gate.md) — блокирующий gate
- [`docs/troubleshooting.md`](docs/troubleshooting.md) — типичные сбои
- [`docs/known-issues.md`](docs/known-issues.md) — чего система **не** утверждает

## Примеры

- [`examples/quick-research.md`](examples/quick-research.md) — QUICK pipeline
- [`examples/deep-research.md`](examples/deep-research.md) — DEEP pipeline
- [`examples/github-research.md`](examples/github-research.md) — provenance-first
- [`examples/model-comparison.md`](examples/model-comparison.md) — adversarial + нормализация бенчмарков
- [`examples/long-form-technical-research.md`](examples/long-form-technical-research.md) — MAX с targeted gap closure

## Структура репозитория

```
DEEP-RESEARCH-SWARM-v0.1.0-beta/
├── README.md             ← этот файл (EN)
├── README.ru.md          ← перевод на русский
├── README.zh-CN.md       ← перевод на китайский (упрощённый)
├── LICENSE               ← MIT
├── CHANGELOG.md
├── SECURITY.md
├── CONTRIBUTING.md
├── agents/               ← живые системные промпты 6 агентов
├── group/                ← групповой промпт, routing, modes, fallback
├── docs/                 ← глубокая документация
├── tests/                ← acceptance + orchestration + secret scan
├── examples/             ← 5 примеров
```

## Источники идей / related work

DEEP RESEARCH SWARM опирается на документированные паттерны из:

- Perplexity Deep Research
- OpenAI Deep Research
- Gemini Deep Research
- Kimi Researcher
- GPT Researcher
- DeerFlow
- LangChain Open Deep Research
- Anthropic multi-agent research (orchestrator-worker, контракт делегирования из 4 полей, effort scaling, LLM-judge рубрика)

Этот репозиторий **не** содержит proprietary промптов перечисленных систем и **не** аффилирован ни с одной из них. Имена используются только для указания на документированные архитектурные паттерны, повлиявшие на дизайн.

## Лицензия

MIT — см. [`LICENSE`](LICENSE).