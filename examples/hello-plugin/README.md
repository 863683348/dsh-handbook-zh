# hello-plugin — 最小示例

一个能跑的最小 DSH 插件，教程 [04-写第一个插件](../docs/04-写第一个插件.md) 的配套代码。

- `package.json` — 声明 `dsh.bundle.patch` 指向 cordis.patch.yml
- `cordis.patch.yml` — 组合补丁：`insert` 插件行
- `lib/index.js` — Cordis 插件：导出 { name, inject, Config, apply }

本地验证：

```bash
dsh plugin --profile <name> add <本目录路径>
dsh --profile <name> --dump-config   # 看 hello 是否进入组合树
```

> 注意：真实插件发布时 `peerDependencies` 要与宿主版本匹配，并加上 `publishConfig.access: public`。
