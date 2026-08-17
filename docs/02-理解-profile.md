# 02 · 理解 profile：DSH 的配置是如何组合出来的

> 一句话总结：profile 是 DSH 的"配置单元"——一个目录里装着插件清单与补丁，启动时按固定顺序把多层 patch 叠加成最终配置树，理解这个叠加顺序（以及用 `--dump-config` 观察它）是玩转 DSH 的关键。

## 1. profile 是什么

`dsh` 本身几乎不做业务：**profile 由多个插件组合包（bundle）的 patch 层按顺序叠加而成，其上再应用用户自己的覆盖配置**。启动一个 profile，就是把这个组合结果交给运行时去执行。

可以这样类比：profile 之于 DSH，就像"环境"之于开发工具——它决定了一套会话里有哪些工具、什么提示词、什么行为。只是在这里，构成环境的不是配置文件里的一个开关，而是一层一层**叠出来的 patch**。

一个 profile 对应 `$DSH_HOME/profiles/<name>` 目录。启动命令：

```powershell
dsh --profile <name>
```

```bash
dsh --profile <name>
```

内置的 `web` 与 `headless` 两个 profile 首次使用时**自动从随附模板初始化**；**其他任何 profile 都必须通过 `dsh plugin` 创建**（详见第 7 节与 [03-插件入门](03-插件入门.md)）。

## 2. profile 目录结构

一个典型的 profile 目录长这样：

```text
$DSH_HOME/profiles/<name>/
├── package.json          # 树外（out-of-tree）插件依赖清单
├── dsh.profile           # profile manifest：元数据 + 按顺序排列的 bundles 列表
├── cordis.patch.yml      # 用户自己的 patch 层
├── node_modules/         # pnpm 安装的树外插件（由 dsh plugin 管理）
└── ...                   # 其他应用数据（会话、日志等）
```

三个关键文件的职责：

| 文件 | 作用 | 由谁维护 |
| --- | --- | --- |
| `package.json` | 声明 profile 依赖的**树外插件**（不在 dsh 安装目录里的插件） | `dsh plugin`（转发 pnpm）自动维护 |
| `dsh.profile` | manifest：元数据 + `bundles` 列表（组合包按顺序排列） | 创建 profile 时生成；插件增删时自动 reconcile |
| `cordis.patch.yml` | 用户自己的 patch 层，追加在组合包 patch 之后 | 你自己手写 |

逐一展开：

- **package.json 的"树外插件"**：指那些不在 dsh 安装目录里的插件包。DSH 安装目录自带官方组合包，第三方插件则作为依赖装进 profile 自己的 `node_modules`。`dsh plugin` 的 add/remove 本质就是在维护这份依赖清单；
- **dsh.profile（manifest）**：记录 profile 的元数据（名字、描述等）和**按顺序排列的 bundles 列表**。`bundles` 列表的顺序就是叠加顺序，插件安装/卸载时该列表会被自动 reconcile（比如 `dsh plugin add` 一个本地目录时会自动把它的组合包加进列表）。manifest 的具体字段格式以官方文档为准；
- **cordis.patch.yml**：你的覆盖层。组合包提供了"出厂配置"，你想改什么、加什么都写在这里。

## 3. 组合包从哪解析

`dsh.profile.bundles` 里列出的组合包，解析顺序是：

1. 先从 **dsh 安装目录**解析内置组合包：`@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-web-app`、`@deepseek-ai/dsh-headless`；
2. 再从 **profile 自身的 node_modules** 解析（pnpm 会把树外插件安装到这个目录）。

为什么要分两步？因为内置组合包随 DSH 版本升级、由官方统一维护，不该被某个 profile 的依赖"绑架"；而第三方插件装在 profile 里，每个 profile 可以有自己的一套（甚至可以装不同版本）。**一个 profile 的插件生态 = 内置组合包 + 树外插件**，这个等式帮你快速判断"某个能力从哪来"。

## 4. 配置层叠加顺序（重点）

配置树以**空根**为起点，依次叠加以下配置层：

```text
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
```

理解要点：

- **先底层后上层，上层覆盖下层**：同一个配置键在多层都出现时，后叠加的层生效。比如官方组合包给某工具设了默认值，你在 profile 的 `cordis.patch.yml` 里改它，就会覆盖出厂值；
- **组合包的 patch 由官方包提供**，不要直接改它们——你的覆盖写在第 2~4 层；
- **`$DSH_HOME/cordis.patch.yml` 是对所有 profile 生效的全局层**：公司统一规范、个人通用偏好放这里；
- **`--patch` 是命令行级临时覆盖**：适合调试，不落盘，重启就没了。

**为什么是"patch 叠加"而不是"一份大配置文件"？** 这是 DSH 插件体系的根基：如果配置是一整份文件，那么每个插件都要"改别人的文件"，装两个插件就会打架。而 patch 是**增量**——每个组合包只声明自己关心的片段，运行时按顺序把它们拼起来，冲突时后层覆盖前层。这保证了：插件可以独立开发、独立发布、任意组合；用户的覆盖永远有地方放（第 2~4 层）；官方升级组合包时不会覆盖掉你的修改。理解了这一点，你就理解了整个 DSH 配置模型。

**一个具体的叠加例子（强烈建议动手试一遍）：**

假设某内置组合包在 patch 里写了某工具的最大重试次数：

```yaml
# 第 1 层（内置组合包的 patch，示意）
- tool-retry:
    maxRetries: 3
```

你在 profile 自己的 `cordis.patch.yml`（第 2 层）里覆盖它：

```yaml
# 第 2 层（profile 自身 cordis.patch.yml）
- tool-retry:
    maxRetries: 5
```

那么 `dsh --profile <name> --dump-config` 里该键的最终值是 **5**——因为第 2 层压在第 1 层之上。而如果第 2 层里没有这一项，最终值就是 3。这个"查最终值"的过程，就是 `--dump-config` 最常用的用途：**它告诉你最终生效的到底是什么，省得你一层层去翻 patch**。

## 5. 启动器 flag 与应用参数

启动器只解析自己的 flag，并把**其后的一切**交给被启动的 profile（由 profile 里的应用插件解析这份共享的不可变参数快照）。因此：

- 启动器 flag 必须写在最前面；
- 启动器无法识别的第一个 token 标志着应用参数的开始。

```powershell
dsh --profile web --port 8080    # --port 属于 web 应用
dsh --profile headless "run the tests"
dsh --profile web --help         # 打印 web 应用的帮助
dsh --help                       # 打印启动器自己的帮助
```

```bash
dsh --profile web --port 8080
dsh --profile headless "run the tests"
dsh --profile web --help
dsh --help
```

> 这条规则很反直觉，却是排查"参数没生效"的第一现场：如果你把 `--port` 写在了 `--profile` 前面（`dsh --port 8080 --profile web`），启动器会把它当自己的 flag 解析掉——参数顺序错了，应用自然收不到。

再往深一层说：启动器拿到应用参数后，会把它包装成一份**共享的不可变参数快照**交给 profile 里的应用插件去解析。这意味着两件事：其一，应用侧的所有插件读到的是**同一份**参数，不会各读各的；其二，这份快照是**只读的**，任何插件都改不了它，避免插件之间互相干扰。所以 `dsh --profile headless "任务"` 里那个任务文本，headless 应用的所有相关插件都能看到同一份；`dsh --profile web --port 8080` 的端口也一样。参数在启动那一刻就"定型"了，之后不会再变。

## 6. --dump-config 实践：看见组合结果

官方提供两个开关，**不启动**就能检查组合后的配置树：

| 开关 | 作用 | 什么时候用 |
| --- | --- | --- |
| `--dump-default-config` | 打印默认配置（不叠加用户覆盖） | 看"出厂"长什么样 |
| `--dump-config` | 打印完整组合后的配置树 | 看你的覆盖有没有生效 |

用 `--dump-config` 检查某个 profile 的最终配置：

```powershell
dsh --profile web --dump-config
```

```bash
dsh --profile web --dump-config
```

把输出存成文件慢慢看：

```powershell
# PowerShell：注意重定向编码，用 Out-File 指定 UTF-8，避免中文乱码
dsh --profile web --dump-config | Out-File -FilePath dump.yml -Encoding utf8
```

```bash
# bash
dsh --profile web --dump-config > dump.yml
```

**怎么读这份输出？** 它是组合后的配置树（YAML/JSON 风格）。核心看两件事：

1. **有没有你要的东西**：装了某个插件后，搜它的 `id` 或包名（例如 `dsh-plugin-focus` 就搜 `focus`），确认组合行存在；
2. **值对不对**：某配置项的值是不是被你的覆盖层改掉了——如果 `--dump-config` 里不是你想要的值，说明你的 patch 层没写对位置（多半是层级顺序问题）。

这是后面验证插件生效的标准方法，03 章会反复用到。

**常见问题：我改了配置，为什么 `--dump-config` 里没变化？** 按下面顺序排查：

1. 是不是改错了文件？profile 级配置在 `$DSH_HOME/profiles/<name>/cordis.patch.yml`，home 级全局配置在 `$DSH_HOME/cordis.patch.yml`——别把两者搞混；
2. 是不是层级太低？如果内置组合包在更上层又写死了同一键，你的覆盖会被压掉；
3. 是不是格式不对？patch 是 YAML，缩进错误会导致整层解析失败（`--dump-config` 会报错或静默跳过）；
4. 是不是没重启？配置在启动时组合，运行中的会话不会热加载（除非用了 HMR 类插件，以官方文档为准）。

## 7. 多 profile 管理

不同场景用不同 profile 是 DSH 的推荐姿势。对比三个常见 profile：

| profile | 初始化方式 | 典型用途 |
| --- | --- | --- |
| `web` | 首次使用自动初始化 | 交互式 Web 界面 |
| `headless` | 首次使用自动初始化 | 脚本化一次性会话 |
| 自定义（如 `dev`、`client-x`） | **必须通过 `dsh plugin` 创建** | 专属插件组合、隔离环境 |

自定义 profile 的创建与插件管理走同一条命令（`dsh plugin` 在 profile 目录里转发给 pnpm）：

```powershell
dsh plugin --profile dev add dsh-plugin-focus
```

```bash
dsh plugin --profile dev add dsh-plugin-focus
```

**多 profile 的典型场景：**

| 场景 | 做法 |
| --- | --- |
| 开发/生产分离 | 开发 profile 装调试插件，生产 profile 只装必需插件 |
| 客户隔离 | 每个客户一套 profile，插件互不影响 |
| 实验 | 临时建 profile 试插件，不满意直接删目录 |

> 注意：自定义 profile 不像 web/headless 那样自动初始化，它依赖 `dsh plugin` 来创建并维护（具体初始化行为以官方文档为准）。给每个场景一套独立 profile，插件的增删互不影响，这是多场景下的基本隔离手段。

**动手练习（5 分钟）：** ① 在 `dsh web` 所在的 profile 里执行 `dsh --profile web --dump-config | Select-String -Pattern "port"`（bash 用 grep），找出 Web 服务的端口配置在哪一层；② 在你的 profile 的 `cordis.patch.yml` 里加一段覆盖该端口的值，重新 dump 确认变成你的值；③ 删掉这段覆盖。做完这三个动作，你对"叠加与覆盖"的体感就建立了。

## 8. 本章小结与检查清单

本章的核心就三句话：**profile 是配置单元，patch 是增量，顺序决定胜负**。只要记住叠加顺序（bundles → profile patch → home patch → --patch）、记住"上层覆盖下层"、记住一切以 `--dump-config` 的最终值为准，你就已经超过了大多数新手。如果只带走一个习惯，那就是：**改任何配置之后，先 `--dump-config` 确认再重启**——它一次回答"有没有、对不对、是不是我要的值"三个问题。下面的清单帮你自测：

## 8.1 本章检查清单

- [ ] 能说清 profile 目录里 `package.json`、`dsh.profile`、`cordis.patch.yml` 各管什么
- [ ] 能背出配置层叠加顺序（bundles → profile patch → home patch → --patch）
- [ ] 知道内置组合包从 dsh 安装目录解析，树外插件从 profile 的 node_modules 解析
- [ ] 会用 `--dump-config` 查看组合结果，并用 `Out-File -Encoding utf8`（PowerShell）保存
- [ ] 会区分 `dsh --help` 与 `dsh --profile web --help`
- [ ] 知道 web/headless 自动初始化、自定义 profile 必须走 `dsh plugin`
- [ ] 理解"上层覆盖下层"，能解释 `--dump-config` 里值不对时从哪一层查起

## 9. 下一步

配置的"容器"理解了，接下来往容器里装东西：下一章 [03-插件入门](03-插件入门.md) 讲怎么找到插件、安装/卸载插件，以及如何验证它真的生效。
