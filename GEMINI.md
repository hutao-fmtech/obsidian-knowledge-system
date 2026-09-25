@AGENTS.md

# Gemini CLI 适配

通用规则全部写在上面引用的 `AGENTS.md` 里，所有 agent 共用；改规则只改那里。

- 开工时先运行 `python3 .agents/scripts/session_brief.py`，拿到交接板、用户画像、经验和仓库状态
- 可复用的能力（skill）在 `.agents/skills/`，读对应的 `SKILL.md` 按步骤执行
