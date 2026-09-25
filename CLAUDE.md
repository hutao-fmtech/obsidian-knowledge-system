# Life Knowledge System - Claude Code 指南

基于 Obsidian 的个人知识管理系统，采用 PARA + MOC + Zettelkasten 混合架构。
完整文档见 `00-系统/📖 使用手册.md`。

## 快速开始

### 创建笔记的基本流程
```bash
# 1. 在 Obsidian 中使用快捷键创建笔记
# - 日记: Cmd+P → "Open today's daily note"
# - 从模板: Cmd+P → "Templater: Create new note from template"

# 2. 或使用命令行创建（从项目根目录）
touch "01-收件箱/快速笔记/临时想法-$(date +%Y%m%d).md"
```

### 常用工作流

**每日捕获流程**
1. 快速想法 → `01-收件箱/快速笔记/`
2. 晚上整理：移至项目/领域/资源，或删除
3. 外部资料 → `04-资源/参考资料/`
4. 深度提炼 → `10-卡片盒/`（用自己的话重写）

**从模板创建笔记**
```
# 在 Obsidian 中
Cmd+P → "Templater: Create new note from template"
选择模板: daily-note-template, work-project-template 等
```

**使用 Dataview 查询**
```dataview
# 查看所有进行中的项目
TABLE project_status, due_date
FROM "02-项目"
WHERE project_status = "active"
SORT due_date ASC

# 查看最近更新的卡片
LIST
FROM "10-卡片盒"
SORT file.mtime DESC
LIMIT 10
```


## 文件夹结构

```
Life-Knowledge-System/
├── 00-系统/          # 系统配置、模板、文档
├── 01-收件箱/        # 临时捕获区,每日清理
│   ├── 快速笔记/     # 临时想法
│   ├── 待处理/       # 保存的资料
│   └── 灵感闪念/     # 创意点子
├── 02-项目/          # PARA-Projects: 有截止日期的目标
│   ├── 工作项目/
│   ├── 个人项目/
│   └── 学习项目/
├── 03-领域/          # PARA-Areas: 持续关注的人生领域
│   ├── 软件工程/     # ⚠️ 独立 Diátaxis 架构（有自己的 CLAUDE.md）
│   ├── 计算机从业/   # 计算机科学基础理论
│   ├── 技术领导力/   # 技术管理与规划
│   ├── 职业发展/
│   ├── 健康管理/
│   ├── 财务规划/
│   ├── 人际关系/
│   ├── 兴趣爱好/
│   └── 读书写作/     # 读书笔记 / 专栏笔记 / 思考写作 / 自省
├── 04-资源/          # PARA-Resources: 外部参考材料
│   ├── 参考资料/     # 查：技术文档 / 方法论 / 调研报告
│   ├── 学习材料/     # 学：文章收藏 / 书摘笔记 / 在线课程 / 教程资料 / 论文笔记
│   ├── 工具箱/       # 用：软件工具 / 在线服务 / 资源导航 / 模板素材
│   ├── 媒体资源/     # 视频、播客笔记
│   └── 链接收藏/     # 还没消化的链接（中转，定期清理）
├── 05-归档/          # PARA-Archives: 按年份归档
├── 10-卡片盒/        # Zettelkasten 永久笔记
│   ├── 概念卡片/     # 核心概念定义
│   ├── 方法卡片/     # 可复用方法论
│   ├── 观点卡片/     # 个人洞察
│   └── 索引卡片/     # MOC 知识地图
├── 20-日志/          # 时间线记录
│   ├── 日记/         # YYYY/MM/YYYY-MM-DD.md
│   ├── 周记/         # YYYY-Wxx.md
│   ├── 月记/         # YYYY-MM.md
│   └── 年记/         # YYYY.md
├── 30-输出/          # 创作成果
│   ├── 微信公众号/   # 公众号文章（含 HTML 版本）
│   ├── 博客文章/     # 学习笔记 / 思考随笔 / 技术博客
│   ├── 技术分享/     # 会议演讲 / 团队分享 / 工作坊
│   ├── 演讲稿/       # 主题演讲 / 即兴演讲
│   └── 作品集/       # 工具作品 / 开源项目 / 设计作品
└── 90-附件/          # 媒体文件
    ├── images/
    │   ├── cover-image/   # 文章封面（按文章 slug 分目录）
    │   ├── illustrations/ # 文章配图（按文章 slug 分目录）
    │   └── prompts/       # 图片生成提示词存档
    ├── files/
    └── audio/
```

## 文件放置决策

新笔记归属规则：有截止日期 → `02-项目/`，需长期关注 → `03-领域/`，外部参考 → `04-资源/`，独立洞察 → `10-卡片盒/`，临时捕获 → `01-收件箱/`。`04-资源/` 内部按使用意图再分：查 → `参考资料/`，学 → `学习材料/`，用 → `工具箱/`。

**槽位契约**：每个目录收什么 `type`，写在它 README frontmatter 的 `slot.accepts` 里（子目录继承上级）。放置笔记前先查契约，`type` 不在 `accepts` 里就换目录。空目录是预留槽位，不要删除。定义见 `00-系统/Frontmatter 规范.md`，全库汇总见 `00-系统/槽位总览.md`。

**移动文件**：在 Obsidian 里移动（拖拽或 `obsidian-cli move`），这样指向它的链接会自动更新；直接 `mv` 会让 wikilink 断掉。
```bash

# 查找缺少 frontmatter 的笔记
grep -L "^---" 01-收件箱/**/*.md
```

## 命名规范

- 日记：`YYYY-MM-DD.md`（路径：`20-日志/日记/YYYY/MM/`）
- 周记：`YYYY-Wxx.md`，月记：`YYYY-MM.md`
- 书籍：`《书名》- 作者.md`，文章：`标题 - 来源 - YYYYMMDD.md`
- **一级目录 README**：`{目录名}-README.md`（如 `01-收件箱-README.md`），避免与子目录 README 混淆

## YAML Frontmatter 规范

完整字段字典见 `00-系统/Frontmatter 规范.md`（`vault-lint` 直接解析其中的类型表和枚举表）。要点：

- 新建笔记包含 `title`、`type`、`created`、`updated`、`tags`；`type` 用英文类型名，取所在目录的 `slot.accepts`
- `status` 只表示文档成熟度：`draft` / `stable` / `deprecated`，不再用中文或 emoji
- 业务进度用独立字段：项目 `project_status`（`planned/active/paused/completed/cancelled`），阅读 `reading_status`（`to_read/reading/completed/paused/abandoned`），领域 `health`（`healthy/attention/at_risk`，必须来自实际评估，未评估就留空）
- 来源用 `sources: [{resource: "<URL 或 [[笔记]]>"}]`，产出者用 `generated: {by, at}`（人写的 `human:<id>`，AI 写的如 `Claude Code/<model>`）

```yaml
---
title: "项目名称"
type: "Project Note"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [项目, 分类]
status: draft
project_status: planned
priority: high
area: 职业发展
start_date: YYYY-MM-DD
due_date: YYYY-MM-DD
---
```

## Obsidian 格式约束

- 笔记间链接使用 `[[笔记名称]]` wikilink 格式
- 内部链接不含扩展名：`[[笔记名]]` 而非 `[[笔记名.md]]`
- 新笔记必须添加至少 2 个双向链接
- 标签格式：`#一级/二级`（如 `#学习/阅读`）

## 模板使用

所有模板在 `00-系统/templates/`：

| 模板文件 | 用途 | 创建位置 |
|---------|------|---------|
| `daily-note-template.md` | 日记 | `20-日志/日记/YYYY/MM/` |
| `work-project-template.md` / `personal-project-template.md` / `learning-project-template.md` | 项目笔记 | `02-项目/` 对应子目录 |
| `reading-note-template.md` | 读书笔记（整本书） | `03-领域/读书写作/读书笔记/` |
| `article-note-template.md` | 文章笔记 | `04-资源/学习材料/文章收藏/` |
| `zettelkasten-{concept,method,opinion}-template.md` | 三类卡片 | `10-卡片盒/` 对应子目录 |
| `moc-template.md` | MOC 索引 | `10-卡片盒/索引卡片/` |
| `area-overview-template.md` | 领域概览 | `03-领域/` |
| `monthly-finance-template.md` | 月度财务记录 | `03-领域/财务规划/` |
| `investment-record-template.md` | 投资操作记录 | `03-领域/财务规划/` |

**使用方式**：Cmd+P → "Templater: Create new note from template" → 选择模板

## 关键插件与使用要点

### Dataview（动态查询）
- 语法：代码块用 `dataview` 标记
- 常用查询：`TABLE`, `LIST`, `FROM`, `WHERE`, `SORT`
- 字段访问：frontmatter 直接写字段名（如 `project_status`），文件属性用 `file.mtime`
- 注意：查询性能依赖 frontmatter 质量

### Templater（模板增强）
- 模板位置：`00-系统/templates/`
- 调用方式：Cmd+P → "Templater: Create new note from template"
- 动态变量：`<% tp.date.now("YYYY-MM-DD") %>` (当前日期)
- ⚠️ 语法严格：`<%` 和 `%>` 之间不能有多余空格

### Calendar（日历视图）
- 点击日期自动创建/打开日记
- 配合 `20-日志/日记/YYYY/MM/` 结构使用

## 维护工具（`.claude/skills/`）

- `vault-lint`：确定性体检脚本（`/usr/bin/python3 .claude/skills/vault-lint/vault_lint.py`），检查 frontmatter、槽位契约和死链；skill 负责分组修复
- `distill`：把收件箱、阅读笔记里可复用的结论提炼成卡片盒卡片，先查重、优先并入已有卡片

## 常见陷阱与注意事项

⚠️ **iCloud Drive 路径包含空格**：CLI 命令中必须用双引号包裹路径
```bash
# ✅ 正确
cd "01-收件箱/快速笔记/"
mv "临时想法.md" "../待处理/"

# ❌ 错误（会失败）
cd 01-收件箱/快速笔记/
```

⚠️ **避免文件锁冲突**：使用 Claude Code 编辑文件时，建议关闭 Obsidian 或确保文件未在 Obsidian 中打开

⚠️ **zsh 通配符**：`**` 模式需要先执行 `setopt globstar`，否则只匹配一层目录

**最后更新**: 2026-09-25
**系统版本**: v1.9
