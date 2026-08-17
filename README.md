# dsh-handbook-zh — DeepSeek Harness 从 0 到 1 系统化中文教程

> 24 小时写书有人看——这是我们对 DeepSeek Harness 生态的判断。本仓库不是又一份"官方文档翻译"，而是一套**面向中文开发者的系统化上手路径**：从安装第一个 profile，到写出并发布自己的插件，全程中文、带命令、带例子、带检查清单。

## 这个仓库是什么

| 内容 | 路径 | 说明 |
| --- | --- | --- |
| 系统化教程（从 0 到 1） | [docs/](docs/) | 按"先跑起来 → 再理解 → 然后改造 → 最后发布"组织 |
| 新手入门包 | [starter/](starter/) | 一键上手的 profile 模板 + 推荐插件清单 + 检查清单 |
| 可运行示例 | [examples/](examples/) | 最小插件 / 工具 / 配置片段 |

## 快速开始（30 秒）

```bash
# 1. 确认已安装 dsh（DeepSeek Harness CLI）
dsh --version

# 2. 启动 Web 界面（首次自动初始化 web profile）
dsh web

# 3. 或跑一次无头会话
dsh --profile headless "你好，介绍一下你自己"

# 4. 管理插件（在 profile 里增删插件）
dsh plugin --profile web add <插件名>
```

> 详见 [docs/01-快速开始.md](docs/01-快速开始.md) ｜ 📕 **整本 PDF**：[dsh-handbook-zh.pdf](dsh-handbook-zh.pdf)（45 页，用 `python scripts/make-pdf.py` 可重新生成）

## 教程目录（docs/）

1. [01-快速开始.md](docs/01-快速开始.md) — 安装、第一个会话、Web 界面
2. [02-理解-profile.md](docs/02-理解-profile.md) — profile 是什么、配置层怎么叠加
3. [03-插件入门.md](docs/03-插件入门.md) — 找插件、装插件、卸载插件
4. [04-写第一个插件.md](docs/04-写第一个插件.md) — 三件套骨架、工具注册、系统提示注入
5. [05-工具开发进阶.md](docs/05-工具开发进阶.md) — JSON Schema、文件读写、生命周期
6. [06-发布插件.md](docs/06-发布插件.md) — npm 发布、GitHub topic、awesome 列表
7. [07-实战案例.md](docs/07-实战案例.md) — 从生态中拆解 3 个真实插件的设计
8. [08-常见问题.md](docs/08-常见问题.md) — 踩坑速查（权限、沙箱、网络、Windows）

## 新手入门包（starter/）

- [starter/profile-template/](starter/profile-template/) — 开箱即用的 profile 目录模板（package.json + dsh.profile + cordis.patch.yml）
- [starter/recommended-plugins.md](starter/recommended-plugins.md) — 精选插件清单（按场景分类）
- [starter/checklist.md](starter/checklist.md) — 新手自查清单（安装 → 首个会话 → 首个插件）

## 关联项目

- 配套插件 [dsh-starter-zh](https://github.com/863683348/dsh-starter-zh)（npm: `dsh-starter-zh`）：安装即得新手引导，与本书内容联动
- 我们在 awesome-dsh-plugin 的插件家族：focus / need-finder / audit / gov / feed / insight / recipe / trend-radar

## 贡献

欢迎 PR 补充教程章节、修正命令、添加新手常见问题。内容规范：命令必须可复制执行；所有路径以 Windows PowerShell 与 bash 双写法给出。

## License

MIT
