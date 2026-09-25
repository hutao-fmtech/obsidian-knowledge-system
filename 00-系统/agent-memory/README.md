---
title: "🧠 Agent 共享记忆"
type: "README"
created: 2026-09-25
updated: 2026-09-25
tags: [系统, agent, 记忆]
status: draft
slot:
  accepts: ["Agent Memory"]
  lifecycle: durable
  owner:
generated:
  by: "Claude Code/claude-opus-5-5"
  at: "2026-09-25T16:00:00+08:00"
---

# 🧠 Agent 共享记忆

> 脑可以换，记忆不随脑走。所有在这个仓库工作的 agent（Claude Code、Codex、Gemini、OpenClaw……）读写同一份记忆，谁接手都知道最近发生了什么、用户是什么样的人、哪里有坑。

规则本身写在根目录 `AGENTS.md`，已经发生的改动由 `git log` 记录。这里只存这两处都存不了的东西：正在进行的状态、还没写进规范的决策、从经验里长出来的认知。

## 结构

| 文件 | 记忆类型 | 内容 | 读取 |
|---|---|---|---|
| [[00-系统/agent-memory/now\|now]] | 工作记忆 | frontmatter 里的路径占用声明 `claims`；正文里待接手的事 | 开工必读 |
| [[00-系统/agent-memory/profile\|profile]] | 用户画像 | 用户的偏好、原则、工作方式 | 开工必读 |
| [[00-系统/agent-memory/lessons\|lessons]] | 经验 | 在这个仓库踩过的坑、验证过的做法 | 开工必读 |
| [[00-系统/agent-memory/persona\|persona]] | 用户人格 | 身份、原则、立场、思维方式、表达风格 | 按需：代表用户做判断或回答时 |
| [[00-系统/agent-memory/decisions\|decisions]] | 决策暂存 | 已拍板、还没写进规范的决策 | 按需 |
| [[00-系统/agent-memory/sessions/README\|sessions/]] | 情景记忆 | 每次有改动或决策的会话一篇 | 看标题，相关才打开 |

三个必读文件合计控制在约 2k tokens。超出时说明有内容该整合进规范、或者该删了。

## 开工

1. 读 `now.md`、`profile.md`、`lessons.md`
2. 运行 `git status`：有不是你做的未提交改动，就不要碰也不要一起提交；再运行 `git log --since=7.days --oneline` 了解最近的改动
3. 浏览 `sessions/` 的文件名，和当前任务相关的才打开读

## 改动前：声明占用

要改的目录可能有其他 agent 同时在碰时，先在 `now.md` 的 frontmatter 里加一条声明：

```yaml
claims:
  - path: "04-资源/"
    by: "claude-code"
    until: "2026-09-25T18:00:00+08:00"   # 最长 4 小时
    why: "重组 04-资源 目录"
```

- 看到别人未过期的声明：避开那些路径，或者先问用户
- 声明已过期（vault-lint 会报 `CLAIM_EXPIRED`）：可以接手，在待接手里写一句谁在什么时候接手了

## 收工

1. 这次有改动或做了决策，就在 `sessions/` 写一篇会话记录（格式见 sessions/README）
2. 更新 `now.md`：撤销自己的占用声明；待接手事项做完的删掉，新产生的加上
3. 新发现的用户偏好、踩到的坑，写进 `profile.md` 或 `lessons.md`，标记 `⏳ 待确认`。用户确认后改成 `✅`。别的 agent 只把 `✅` 的条目当作事实

## 写入规则

- 每条记忆都要注明来源（会话记录链接或用户原话）和日期
- profile 和 persona 的条目带优先级标签 `[CORE]` / `[PRINCIPLE]` / `[PREFERENCE]`，冲突时按这个顺序取舍；`[CORE]` 只能由用户亲口确立或修改，agent 不能自行把条目升为 CORE
- 已经写进 `AGENTS.md`、README 或规范的内容，这里不要再重复；写进去以后就把这里的条目删掉，最多留一句指针
- 不记录密码、token、密钥等敏感信息
- profile 只记用户明确说过、或者多次观察到的偏好，不记一次性的临时要求

## 整合与遗忘

- **定期整合**：每周（或定期）读一遍会话记录，把决策写进规范、偏好写进 profile、经验写进 lessons，然后把会话记录归档到 `05-归档/agent-sessions/`
- **自动提醒**：会话记录超过 30 天、占用声明过期，vault-lint 都会提醒
- **主动遗忘**：profile、lessons 里过时或被推翻的条目直接删掉，不要留着"曾经"
