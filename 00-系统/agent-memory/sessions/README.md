---
title: "🗂️ 会话记录"
type: "README"
created: 2026-09-25
updated: 2026-09-25
tags: [系统, agent, 记忆]
status: draft
slot:
  accepts: ["Agent Session"]
  lifecycle: transient
  max_age_days: 30
  owner:
generated:
  by: "Claude Code/claude-opus-5-5"
  at: "2026-09-25T16:00:00+08:00"
---

# 🗂️ 会话记录

每次有改动或做了决策的 agent 会话写一篇，记下 `git log` 里看不到的东西：为什么这么做、否掉了什么方案、用户说了什么、什么没做完。纯问答、没有改动的会话不用写。

定期整合后归档到 `05-归档/agent-sessions/`；超过 30 天没整合，vault-lint 会提醒。协议见 [[00-系统/agent-memory/README|记忆协议]]，待接手事项同步到 [[00-系统/agent-memory/now|交接板]]。

## 格式

文件名 `YYYY-MM-DD-<harness>-<主题>.md`，40 行以内：

```markdown
---
title: "会话：<主题>"
type: "Agent Session"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [系统, agent, 会话]
generated:
  by: "<harness>/<model>"
  at: "<ISO 时间>"
---

## 意图        用户要解决什么
## 结果        做成了什么，列出提交号
## 决策与理由  拍板的事和为什么
## 放弃的方案  考虑过但没采用的，以及原因
## 用户反馈    纠正、偏好、原话
## 遗留        没做完的事（同步到 now.md）
```
