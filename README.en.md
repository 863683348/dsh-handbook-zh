# dsh-handbook-zh — DeepSeek Harness 0→1 Systematic Chinese Tutorial

> A 24-hour book gets readers — that is our read on the DeepSeek Harness ecosystem. This repo is not another translation of the official docs, but a **systematic on-ramp for Chinese-speaking developers**: from installing your first profile to writing and publishing your own plugin, all in Chinese, with commands, examples, and checklists.

> 中文版：本仓库默认语言为中文，README 见 [README.md](README.md)。

## What's inside

| Content | Path | Description |
| --- | --- | --- |
| Systematic tutorial (0→1) | [docs/](docs/) | Organized as: run it → understand it → change it → ship it |
| Beginner starter pack | [starter/](starter/) | Profile template + recommended plugin list + self-check checklist |
| Runnable examples | [examples/](examples/) | Minimal plugin / tool / config snippets |
| PDF edition | [dsh-handbook-zh.pdf](dsh-handbook-zh.pdf) | 45-page PDF (cover + TOC + 8 chapters), regenerate with `python scripts/make-pdf.py` |

## Quick start (30 seconds)

```bash
dsh --version                 # 1. confirm dsh is installed
dsh web                       # 2. launch the Web UI (auto-initializes the web profile)
dsh --profile headless "hi"   # 3. or run a one-shot headless session
dsh plugin --profile web add <plugin>   # 4. manage plugins per profile
```

## Tutorial chapters (docs/)

1. [01-quickstart](docs/01-快速开始.md) — install, first session, Web UI
2. [02-understanding-profile](docs/02-理解-profile.md) — profiles & config layer stacking
3. [03-plugin-basics](docs/03-插件入门.md) — find / install / remove plugins
4. [04-first-plugin](docs/04-写第一个插件.md) — the three-file skeleton & hello tool
5. [05-advanced-tools](docs/05-工具开发进阶.md) — JSON Schema, ctx.fs, lifecycle
6. [06-publishing](docs/06-发布插件.md) — npm publish, GitHub topic, awesome list
7. [07-case-studies](docs/07-实战案例.md) — 3 real plugins dissected
8. [08-faq](docs/08-常见问题.md) — gotcha quick-reference

## Companion plugin

- [dsh-starter-zh](https://github.com/863683348/dsh-starter-zh) (npm: `dsh-starter-zh`) — install it and your agent walks you through the 0→1 path in-session.

## License

MIT
