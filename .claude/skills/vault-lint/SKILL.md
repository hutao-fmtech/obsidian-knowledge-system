---
name: vault-lint
description: 知识库体检：用确定性脚本检查 frontmatter、槽位契约和死链，分组给出修复建议，确认后修复并提交。当用户说 /vault-lint、体检、检查知识库、lint、查死链时使用；定期整理时也可以先跑一遍脚本看汇总。
---

# vault-lint 工作流

判定只看脚本输出，不凭印象加规则。脚本从 `00-系统/Frontmatter 规范.md` 解析 type 表、`status` 枚举和业务状态枚举，规则要变先改规范。

## 第 1 步：运行脚本

```bash
/usr/bin/python3 .claude/skills/vault-lint/vault_lint.py            # 展开 error + warn
/usr/bin/python3 .claude/skills/vault-lint/vault_lint.py --path 04-资源 --limit 0
/usr/bin/python3 .claude/skills/vault-lint/vault_lint.py --json      # 需要逐条处理时
```

系统自带的 `/usr/bin/python3` 有 PyYAML，其他 python3 没有；都不行时用 `uv run .claude/skills/vault-lint/vault_lint.py`。退出码 1 表示存在 error。

## 第 2 步：分诊（一轮确认，不逐条打断）

按下表给每组问题提出处理方式，用一张表呈现「规则 / 数量 / 建议动作 / 需要用户判断的项」，一次性确认。

| 规则 | 级别 | 处理 |
|------|------|------|
| `TYPE_UNKNOWN` | error | 按映射改 type：`文章阅读笔记` / `帖子阅读笔记` / `文章学习笔记` / `literature-note` → `Article Note`；`论文阅读笔记` → `Paper Note`；`工具笔记` → `Tool Note`；`调研报告` → `Reference`。映射外的值读正文判断 |
| `TYPE_MISSING` | error | 从所在槽位的 `accepts` 里选；候选不止一个时读正文判断 |
| `TYPE_NOT_IN_SLOT` | error | 三选一：**type 标错**→改 type；**放错位置**→移到 type 对应的槽位；**契约太窄**→属于结构调整，只列出来交给用户，不自行扩 `accepts`。例：`01-计算机系统` 里的概念卡片，内容是原子化卡片就移到 `10-卡片盒`，内容是领域学习记录就改成 `Area Note` |
| `SLOT_INVALID` | error | 修契约本身；属于结构调整，先确认 |
| `FM_PARSE` | error | 读 frontmatter 修 YAML 语法（最常见：值里有冒号却没加引号） |
| `BUSINESS_ENUM` / `STATUS_LEGACY` | error / warn | 按 Frontmatter 规范迁移：旧值的业务含义挪到独立字段，`status` 只留 `draft/stable/deprecated`。AI agent 写入的 `待归档`、`pending` 这类值 → `status: draft`。`health` 的 emoji 值只有确实是评估记录才映射（🟢→`healthy`），含义不明的保留原值，列为待用户决定 |
| `DATE_FORMAT` | warn | 截成 `YYYY-MM-DD` |
| `LEGACY_FIELD`（`ai_source`） | warn | 改成 `generated: {by: <原值>, at: "<created>T00:00:00Z"}`，然后删掉 `ai_source`。已有 `generated` 时：`by` 是批量迁移时填的默认人类身份（如 `human:<id>`）而 `ai_source` 指向 AI，就把 `by` 改为 `ai_source` 的值（真实来源优先），其余情况保留原 `generated` |
| `DEAD_LINK` | warn | 先在全库按文件名找目标（目录重组后路径变了）→ 改成现有路径；找不到的，README 里的导航链接改指向现有入口或删掉；缺失的附件列给用户 |
| `TRANSIENT_AGE` / `ACTIVE_DONE` | warn | 不在这里处理，交给定期整理（收件箱分诊、项目归档） |
| info 级（`FIELD_MISSING`、`WANTED_NOTE`、`SLOT_OWNER_MISSING`、`source` 类旧字段） | info | 只报数量，不修。规范要求历史笔记随编辑补齐，不批量改写；`WANTED_NOTE` 是 Obsidian 里指向"待写笔记"的正常链接 |

## 第 3 步：执行

- 改 frontmatter 只动相关字段，不重排、不改其他字段；只改元数据时不更新 `updated`（它表示内容更新）
- 移动文件要通过 Obsidian（或 `obsidian-cli move`）完成，这样链接会自动更新；不要直接 `mv`，否则指向它的 wikilink 会断
- `05-归档/` 不修（契约为 frozen，脚本也不检查）
- 用户没确认的组不动

## 第 4 步：复跑并提交

1. 复跑脚本，汇报修复前后各级别的数量；error 没清零的，说明剩下的是什么、为什么没修
2. 使用 git 管理时提交，标题形如 `体检(04-资源): vault-lint 修复 12 处 type 与 8 条死链`。只 add 本次修过的文件，其他工具新写入的笔记不要带上
