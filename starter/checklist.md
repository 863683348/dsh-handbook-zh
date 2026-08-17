# 新手自查清单（Checklist）

> 每完成一项打个勾。全部打勾 ≈ 你已经可以独立在 DSH 生态里干活了。

## 安装与运行

- [ ] 能启动 `dsh web` 或 `dsh --profile headless "..."` 会话
- [ ] 知道 `dsh --profile <name>` 是启动指定 profile

## Profile 理解

- [ ] 知道 profile 目录包含 package.json / dsh.profile / cordis.patch.yml
- [ ] 会看 `--dump-config` 输出，能指出某个插件行来自哪个配置层
- [ ] 理解配置层叠加顺序：bundles → profile cordis.patch.yml → home 级 patch → --patch 覆盖

## 插件操作

- [ ] 成功安装过一个插件到 profile（`dsh plugin --profile <name> add <plugin>`）
- [ ] 知道如何卸载插件
- [ ] 在会话里让模型调用过至少一个插件提供的工具

## 插件开发

- [ ] 理解三件套：package.json（dsh.bundle.patch）+ cordis.patch.yml + lib/index.js
- [ ] 写出过一个最小插件（注册一个工具）并在本地验证
- [ ] 了解 ctx.fs 与工作区 containment 校验

## 发布

- [ ] 了解 npm publish 流程与 token 注意事项
- [ ] 了解 GitHub dsh-plugin topic 的作用
- [ ] 了解 awesome-dsh-plugin 收录要求（bundle 声明 / ≥1 天 / ≥10 commits）

## 求助渠道

- [ ] 知道官方文档位置（deepseek-ai/deepseek-harness）
- [ ] 会查本教程 08-常见问题 的踩坑速查表
