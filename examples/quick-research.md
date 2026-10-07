# Example 1 — Quick research

> Mode: ⚡ QUICK

## User query

> What's the latest stable version of Ollama and on which platforms does it run natively?

## What happens

1. **Curator** auto-picks `⚡ QUICK`. Single workstream.
2. **Curator** runs the QUICK search plan alone (or dispatches one quick task to either Scout or Hunter — protocol HF-1).
3. **Primary source check** is done against the project's own release page and the README. The first-source URL is opened.
4. **Light verification** — does the README mention all four target platforms? Date match?
5. **Short synthesis** in the QUICK output format.

## Expected output

```
## ⚡ Короткий ответ
Latest Ollama stable is <version>, released <date>. Native installers are
available for macOS, Linux, and Windows; Docker is supported but not required.

## Главное
- Version: <version>
- Released: <date>
- Native installers: macOS · Linux · Windows
- Docker: supported (optional)
- Models: GGUF, Q4_K_M average ~2–8 GB

## 📊 Сравнение
(n/a — single product)

## 💡 Вывод
Для большинства сценариев рекомендую ставить нативно и сразу тестировать
через `ollama run <model>`.

## 📚 Источники
- https://ollama.com/release/<version>
- https://github.com/ollama/ollama/blob/main/README.md
- https://ollama.com/download

Проверено: 3 источника · <date>
```

## Why QUICK and not DEEP?

The user asked one factual question. The mode ladder auto-selection rule says:

> "what is the latest version of X?" → QUICK

DEEP would over-spend: 20–50 sources for a version number is not justified.