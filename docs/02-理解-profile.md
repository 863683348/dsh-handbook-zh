# 02 · 理解 profile：DSH 的配置是如何组合出来的

> 一句话总结：profile 是 DSH 的"配置单元"——一个目录里装着插件清单与补丁，启动时按固定顺序把多层 patch 叠加成最终配置树，理解这个叠加顺序（以及用 \`--dump-config\` 观察它）是玩转 DSH 的关键。

## 1. profile 是什么

\`dsh\` 本身几乎不做业务：**profile 由多个插件组合包（bundle）的 patch 层按顺序叠加而成，其上再应用用户自己的覆盖配置**。启动一个 profile，就是把这个组合结果交给运行时去执行。

一个 profile 对应 \`$DSH_HOME/profiles/<name>\` 目录。启动命令：

\`\`\`powershell
dsh --profile <name>
\`\`\`

\`\`\`bash
dsh --profile <name>
\`\`\`

内置的 \`web\` 与 \`headless\` 两个 profile 首次使用时**自动从随附模板初始化**；**其他任何 profile 都必须通过 \`dsh plugin\` 创建**（详见第 7 节与 [03-插件入门](03-插件入门.md)）。

## 2. profile 目录结构

一个典型的 profile 目录长这样：

\`\`\`text
$DSH_HOME/profiles/<name>/
├── package.json          # 树外（out-of-tree）插件依赖清单
├── dsh.profile           # profile manifest：元数据 + 按顺序排列的 bundles 列表
├── cordis.patch.yml      # 用户自己的 patch 层
├── node_modules/         # pnpm 安装的树外插件（由 dsh plugin 管理）
└── ...                   # 其他应用数据（会话、日志等）
\`\`\`

三个关键文件的职责：

| 文件 | 作用 | 由谁维护 |
| --- | --- | --- |
| \`package.json\` | 声明 profile 依赖的**树外插件**（不在 dsh 安装目录里的插件） | \`dsh plugin\`（转发 pnpm）自动维护 |
| \`dsh.profile\` | manifest：元数据 + \`bundles\` 列表（组合包按顺序排列） | 创建 profile 时生成；插件增删时自动 reconcile |
| \`cordis.patch.yml\` | 用户自己的 patch 层，追加在组合包 patch 之后 | 你自己手写 |

- **bundles 列表**决定启动时把哪些组合包的 patch 叠进来，顺序就是叠加顺序；
- **cordis.patch.yml** 是"你的覆盖层"：在 bundles 提供的默认配置之上，做插入、修改、覆盖。

## 3. 组合包从哪解析

\`dsh.profile.bundles\` 里列出的组合包，解析顺序是：

1. 先从 **dsh 安装目录**解析内置组合包：\`@deepseek-ai/dsh-base\`、\`@deepseek-ai/dsh-web-app\`、\`@deepseek-ai/dsh-headless\`；
2. 再从 **profile 自身的 node_modules** 解析（pnpm 会把树外插件安装到这个目录）。

内置组合包负责 DSH 的"出厂配置"：基础运行时（base）、Web 界面（web-app）、无头会话（headless）。你装的第三方插件则全部落在 profile 的 \`node_modules\` 里。**所以一个 profile 的插件生态 = 内置组合包 + 树外插件**。

## 4. 配置层叠加顺序（重点）

配置树以**空根**为起点，依次叠加以下配置层：

\`\`\`text
空根 (empty root)
  │
  ▼ 第 1 层：dsh.profile.bundles 中各组合包的 patch（按 bundles 列表顺序）
  │
  ▼ 第 2 层：profile 自身的 cordis.patch.yml
  │
  ▼ 第 3 层：$DSH_HOME/cordis.patch.yml（home 级全局覆盖）
  │
  ▼ 第 4 层：--patch 指定的覆盖层
  │
  ▼ 最终配置树
\`\`\`

理解要点：

- **先底层后上层，上层覆盖下层**：后叠加的层可以覆盖/修改先叠加的层；
- 组合包的 patch 由官方包提供，**不要直接改它们**——你的覆盖写在第 2~4 层；
- \`$DSH_HOME/cordis.patch.yml\` 是对**所有 profile 生效**的全局层；
- \`--patch\` 是命令行级的临时覆盖，适合调试，不落盘。

## 5. 启动器 flag 与应用参数

启动器只解析自己的 flag，并把**其后的一切**交给被启动的 profile（由 profile 里的应用插件解析这份共享的不可变参数快照）。因此：

- 启动器 flag 必须写在最前面；
- 启动器无法识别的第一个 token 标志着应用参数的开始。

\`\`\`powershell
dsh --profile web --port 8080    # --port 属于 web 应用
dsh --profile headless "run the tests"
dsh --profile web --help         # 打印 web 应用的帮助
dsh --help                       # 打印启动器自己的帮助
\`\`\`

\`\`\`bash
dsh --profile web --port 8080
dsh --profile headless "run the tests"
dsh --profile web --help
dsh --help
\`\`\`

## 6. --dump-config 实践：看见组合结果

官方提供两个开关，**不启动**就能检查组合后的配置树：

| 开关 | 作用 |
| --- | --- |
| \`--dump-default-config\` | 打印默认配置（不叠加用户覆盖） |
| \`--dump-config\` | 打印完整组合后的配置树 |

用 \`--dump-config\` 检查某个 profile 的最终配置，并顺便验证你装的插件是否进了组合树：

\`\`\`powershell
dsh --profile web --dump-config
\`\`\`

\`\`\`bash
dsh --profile web --dump-config
\`\`\`

把输出存成文件慢慢看：

\`\`\`powershell
# PowerShell：注意重定向编码，用 Out-File 指定 UTF-8，避免中文乱码
dsh --profile web --dump-config | Out-File -FilePath dump.yml -Encoding utf8
\`\`\`

\`\`\`bash
# bash
dsh --profile web --dump-config > dump.yml
\`\`\`

在输出里搜插件的 \`id\` 或包名（例如装了 \`dsh-plugin-focus\` 就搜 \`focus\`），确认组合行存在——这是后面 [03-插件入门](03-插件入门.md) 验证插件生效的标准方法。

## 7. 多 profile 管理

不同场景用不同 profile 是 DSH 的推荐姿势。对比三个常见 profile：

| profile | 初始化方式 | 典型用途 |
| --- | --- | --- |
| \`web\` | 首次使用自动初始化 | 交互式 Web 界面 |
| \`headless\` | 首次使用自动初始化 | 脚本化一次性会话 |
| 自定义（如 \`dev\`、\`client-x\`） | **必须通过 \`dsh plugin\` 创建** | 专属插件组合、隔离环境 |

自定义 profile 的创建与插件管理走同一条命令（\`dsh plugin\` 在 profile 目录里转发给 pnpm）：

\`\`\`powershell
dsh plugin --profile dev add dsh-plugin-focus
\`\`\`

\`\`\`bash
dsh plugin --profile dev add dsh-plugin-focus
\`\`\`

> 注意：自定义 profile 不像 web/headless 那样自动初始化，它依赖 \`dsh plugin\` 来创建并维护（具体初始化行为以官方文档为准）。给每个客户/每个项目一套独立 profile，插件的增删互不影响，这是多租户场景下的基本隔离手段。

## 8. 本章检查清单

- [ ] 能说清 profile 目录里 \`package.json\`、\`dsh.profile\`、\`cordis.patch.yml\` 各管什么
- [ ] 能背出配置层叠加顺序（bundles → profile patch → home patch → --patch）
- [ ] 知道内置组合包从 dsh 安装目录解析，树外插件从 profile 的 node_modules 解析
- [ ] 会用 \`--dump-config\` 查看组合结果，并用 \`Out-File -Encoding utf8\`（PowerShell）保存
- [ ] 会区分 \`dsh --help\` 与 \`dsh --profile web --help\`
- [ ] 知道 web/headless 自动初始化、自定义 profile 必须走 \`dsh plugin\`

## 9. 下一步

配置的"容器"理解了，接下来往容器里装东西：下一章 [03-插件入门](03-插件入门.md) 讲怎么找到插件、安装/卸载插件，以及如何验证它真的生效。
