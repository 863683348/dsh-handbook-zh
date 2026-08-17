# profile 模板使用说明

1. 把本目录复制到 `$DSH_HOME/profiles/<你的profile名>/`
2. 编辑 package.json：dependencies 加你想要的插件（npm 包名）
3. 编辑 package.json 的 dsh.profile.bundles：把插件名加进列表（顺序即叠加顺序）
4. 运行 `dsh --profile <你的profile名>` 启动

> 提示：`$DSH_HOME` 通常是 `~/.dsh`（Windows 上为 `%USERPROFILE%\.dsh`）。
