---
title: "Agent 操作指南"
created: 2026-03-01
updated: 2026-09-25
type: "machine-index"
tags:
  - 指南
  - 仓库规范
---

# Life Knowledge System - Agent 操作指南

> 本文件是所有 AI agent 在这个仓库里工作的**唯一规则来源**，适用于 Claude Code、Codex、Gemini、OpenClaw 等。
>
> - Claude Code、Gemini CLI 分别通过根目录 `CLAUDE.md`、`GEMINI.md` 里的 `@AGENTS.md` 读取本文件
> - 子目录的 `AGENTS.md` 补充该目录自己的规则
> - 修改规则只改这里；各 harness 的专属文件只放适配性内容

这是一个基于 Obsidian 的个人知识管理系统，采用 PARA + MOC + Zettelkasten 混合架构。完整说明见 `00-系统/📖 使用手册.md`。

## 共享记忆

所有 agent 共用一份记忆：`00-系统/agent-memory/`。脑可以换，记忆不随脑走。完整的读写协议见该目录的 README。

**开工**：
1. 运行 `python3 .agents/scripts/session_brief.py`，一次拿到开工简报：`00-系统/agent-memory/` 下的 `now.md`（交接板）、`profile.md`（用户画像）、`lessons.md`（经验与陷阱），加上仓库状态（未提交的改动、近 7 天的提交）。需要代表用户做判断或回答时，再读 `persona.md`
2. 简报里如果有不是你做的未提交改动，说明可能有其他 agent 正在工作：不要改动这些文件，也不要把它们和你的改动一起提交
3. 读目标目录的 README（`README.md` 或 `XX-目录名-README.md`）。如果该目录有 `AGENTS.md`，也一并读
4. 新建长期笔记之前，先看 `01-收件箱/` 里有没有相关内容需要一起处理

**改动前**：要改的目录可能有其他 agent 同时在碰时，先在 `now.md` 的 frontmatter `claims` 里声明占用（路径、谁、到期时间、原因）。看到别人未过期的声明就避开，或者先问用户。

**收工**：有改动或做了决策，就在 `00-系统/agent-memory/sessions/` 写一篇会话记录；更新 `now.md`，撤销占用声明、增删待接手事项。新发现的用户偏好或坑写进 `profile.md` 或 `lessons.md`，标记 `⏳ 待确认`，用户确认后才算数。

另外三条：
- 不在根目录建笔记
- 不改 `.obsidian/`，除非用户明确要求
- `.git/`、`.trash/`、`.obsidian/` 当作系统内部目录，不要碰

## 放置决策

先按下面的归属规则决定去哪个顶层目录：

| 内容 | 去向 |
|---|---|
| 有截止日期、明确交付物或执行责任人 | `02-项目/` |
| 需要长期关注的责任或能力领域 | `03-领域/` |
| 以备查阅的外部资料 | `04-资源/` |
| 独立的洞察、概念、方法或观点 | `10-卡片盒/` |
| 临时捕获，或者还拿不准放哪 | `01-收件箱/` |
| 对外发布的成品 | `30-输出/` |
| 已完成、不再活跃、只留作记录 | `05-归档/` |

拿不准时先放收件箱，不要过早硬定一个长期位置。

**读书写作分两层**：日常读书写作（不一定发布）放 `03-领域/读书写作/`，里面分读书笔记、专栏笔记、思考写作、自省；对外发布的成品放 `30-输出/`。

**槽位契约**：
- 每个目录收哪些 `type`，以它 README frontmatter 里的 `slot.accepts` 为准；子目录继承上级
- 放置笔记前先查契约。`type` 不在 `accepts` 里，就换一个目录，或者先向用户确认
- 空目录是预留的槽位，不要删除
- 定义见 `00-系统/Frontmatter 规范.md`，全库汇总见 `00-系统/槽位总览.md`

## 核心工作流

- **每日捕获**：
  - 快速想法 → `01-收件箱/快速笔记/`
  - 外部资料 → `04-资源/`
  - 深度提炼（用自己的话重写）→ `10-卡片盒/`
- **每周整理**：清空收件箱、写周记、把本周的 agent 会话记录整合进共享记忆。流程稳定后，可以写成 `.agents/skills/` 下的一个 skill

## 命名规范

- 日记 `YYYY-MM-DD.md`，放在 `20-日志/日记/YYYY/MM/`；周记 `YYYY-Wxx.md`；月记 `YYYY-MM.md`
- 书籍 `《书名》- 作者.md`；文章 `标题 - 来源 - YYYYMMDD.md`
- 卡片：概念卡用概念名；方法卡、观点卡用结论式标题（如"离职前先区分环境问题和个人问题"）
- README：顶层目录（01~90-）用 `XX-目录名-README.md`（如 `04-资源-README.md`），所有子目录统一用 `README.md`

## Frontmatter

字段字典、类型枚举和迁移历史见 `00-系统/Frontmatter 规范.md`，vault-lint 会直接解析这份文档。

**基础字段**：
- 新建笔记包含 `title`、`type`、`created`、`updated`、`tags`；`tags` 用中文
- 修改内容时更新 `updated`。只改元数据时不更新
- 历史笔记缺字段的，等编辑到那篇时再补齐，用已有的日期证据，不要编造日期

**状态字段**：
- `status` 只表示文档成熟度：`draft` / `stable` / `deprecated`
- 业务进度用独立字段：项目用 `project_status`，阅读用 `reading_status`，领域健康度用 `health`
- 无法确认的留空，不能从文档成熟度去推断业务进度
- 字段有调整时，同步修改模板和看板查询

**agent 写入的笔记**：
- 产出来源写成 `generated: {by: "<Agent 名>", at: "<ISO 时间>"}`。`ai_source` 已停用
- 出处写成 `sources: [{resource: "<URL 或渠道>"}]`，不用平铺的 `source` / `url`
- `type` 取目标目录 `slot.accepts` 里的值。收件箱的文章笔记用 `Article Note`，思考捕获用 `Inbox Capture`；以后移出收件箱时，按新目录调整 `type`
- 新笔记用 `status: draft`。归档意图（比如"周末归档建议"）写在正文里，不要写进 `status`

**隐私**：笔记里含证件号、密码、手机号、密钥或他人联系方式时，显式标 `visibility: "🔒 私有"`；这类笔记**禁止改成 `🌐 可公开`**，也不能作为 `30-输出/` 的素材。

`visibility`、`Attested Computation` 等按需字段见规范；注意 Attested Computation 只用于需要反复按同一公式计算、并能校验算没算错的数值，一次性判断或分析不要用。

## Obsidian 格式与编辑守则

- 笔记之间用 `[[笔记名称]]` wikilink 链接，不带 `.md` 扩展名
- 新建的长期笔记至少加 2 个双向链接，不要留成孤岛
- 标签格式 `#一级/二级`（如 `#学习/阅读`）
- 模板里有 emoji 标题的，保持原样
- 优先改进已有笔记，不要新建重复的笔记
- 附件放在 `90-附件/`
- **移动或重命名笔记必须用 `obsidian-cli move <源> <目标>`**：位置参数，不带扩展名，用 vault 内的相对路径。直接 `mv` 会让所有 wikilink 失效。已知的陷阱见 `.agents/skills/obsidian-cli-usage/SKILL.md`
- 不要随意改目录名，现有链接都依赖稳定的路径

## 模板（`00-系统/templates/`）

新笔记放到哪个目录，以槽位契约为准。

⚠️ Templater 语法很严格：`<%` 与 `%>` 之间不能有多余的空格。

## HOME 待办机制（`00-系统/🏠 HOME.md`）

- 待办查询按 `tags: [todo]` 过滤：只有 frontmatter 含 `todo` 标签的文件才会出现在 HOME 待办里
- 周期性事项不用 `- [ ]`，改用普通列表，避免"一勾选就消失"

## 能力（可复用的手）

skill 是纯 markdown 写成的流程说明，统一放在中立目录 `.agents/skills/`，任何 agent 都可以直接读对应的 `SKILL.md`，按步骤执行。各 harness 的专属目录只做链接，不存放实体文件：比如 `.claude/skills` 是指向这里的软链接，Claude Code 通过它自动发现 skill、用 `/<name>` 调用。新增或修改 skill 只在 `.agents/skills/` 下进行。

有哪些能力：列出 `.agents/skills/` 目录，读每个 `SKILL.md` 开头的 `description`，那里写了用途和什么时候用。

**校验**：改完之后运行 `python3 .agents/skills/vault-lint/vault_lint.py --path <你改过的目录> --level error`，你改的文件不能出现在输出里。vault-lint 依赖 PyYAML：先 `pip install pyyaml`，或者用 `uv run` 运行。

## 提交

- 提交信息写清为什么改、改了什么；格式可以按自己的习惯定，比如中文 `type(scope): subject`
- 提交信息末尾加一行 `Agent: <harness>/<model>`（如 `Agent: codex/gpt-5.5`），标明是哪个 agent 做的
- 只提交自己改过的文件。其他 agent 新写入的笔记不要一起提交
- 只在用户要求时提交；推送更要用户明确同意

## 常见陷阱

- **路径含空格**：vault 放在 iCloud 时，路径里有空格和中文，命令行里一律用双引号包住路径
- **文件锁冲突**：编辑前确认该文件没有在 Obsidian 中处于编辑状态
- **zsh 通配符**：`**` 需要先执行 `setopt globstar`，否则只匹配一层目录

## 写 README 和 AGENTS.md

- **AGENTS.md** 只写从仓库里推导不出来的东西：陷阱、约定、判断规则、禁止事项。目录结构树、文件清单、`ls`/`grep` 这类命令示例一律不写；某类任务专用的参考资料放进 skill，按需读取。CLAUDE.md 等 harness 专属文件只放适配性内容
- 写或改 README 之前，先读 `00-系统/README-写作范式.md`（README 的角色、该写什么不该写什么、章节格式都在那里）。**结构调整必须先和用户确认，不能自作主张删减或重组章节。**

**最后更新**: 2026-09-25
**系统版本**: v2.0
