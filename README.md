# Life Knowledge System

基于 **PARA + MOC + Zettelkasten** 的个人知识管理系统，使用 Obsidian 构建。

## 快速上手

1. 用 Obsidian 打开本目录（「打开文件夹作为库」）
2. 安装并启用必要插件（见下方说明）
3. 打开 `00-系统/📖 使用手册.md` 查看完整说明

## 插件安装与启用

本系统的模板功能依赖以下社区插件，**缺少任何一个都会导致模板无法正常运行**。

### 必装插件

| 插件名 | 插件 ID | 用途 |
|--------|---------|------|
| Templater | `templater-obsidian` | 驱动所有模板，提供动态日期、路径等变量 |
| Dataview | `dataview` | 动态查询笔记，生成项目列表、进度看板等 |
| Calendar | `calendar` | 日历视图，点击日期创建/打开日记 |
| Excalidraw | `obsidian-excalidraw-plugin` | 手绘风格白板，用于思维导图和草图 |

### 可选插件（推荐）

| 插件名 | 插件 ID | 用途 |
|--------|---------|------|
| Kanban | `obsidian-kanban` | 看板视图，管理项目任务卡片 |
| Tasks | `obsidian-tasks-plugin` | 任务管理，支持截止日期与重复任务 |
| QuickAdd | `quickadd` | 快速捕获想法，一键创建笔记 |

### 安装步骤

1. 打开 Obsidian → **设置（⚙️）** → **社区插件**
2. 关闭「安全模式」（首次需确认）
3. 点击「浏览」，搜索上表中的插件名称
4. 逐一点击「安装」，安装后点击「启用」

### Templater 必要配置

安装 Templater 后，需要指定模板目录，否则无法使用本系统的模板：

1. 设置 → **Templater** → **Template folder location**
2. 填入：`00-系统/templates`
3. 建议同时开启 **「Trigger Templater on new file creation」**

> [!tip] 验证是否安装成功
> 按 `Cmd+P`，输入 `Templater`，如果能看到 "Create new note from template" 选项，说明插件已正确安装并配置。

## 目录结构

```
├── 00-系统/        # 模板、主页、使用手册
├── 01-收件箱/      # 临时捕获区（每日清理）
├── 02-项目/        # 有截止日期的目标
├── 03-领域/        # 持续关注的人生领域
├── 04-资源/        # 外部参考材料
├── 05-归档/        # 按年份归档
├── 10-卡片盒/      # Zettelkasten 永久笔记
├── 20-日志/        # 日记 / 周记 / 月记 / 年记
├── 30-输出/        # 博客、公众号等创作成果
└── 90-附件/        # 图片、文件、音频
```

## License

MIT — 随意使用和修改，保留出处即可。
