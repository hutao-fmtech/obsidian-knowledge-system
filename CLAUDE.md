@AGENTS.md

# Claude Code 适配

通用规则全部写在上面引用的 `AGENTS.md` 里，所有 agent 共用；改规则只改那里。本文件只放 Claude Code 专有的内容：

- skill 的实体文件在 `.agents/skills/`。`.claude/skills` 只是指向它的软链接，这样 Claude Code 能自动发现 skill，用 `/<name>` 调用，比如 `/vault-lint`、`/distill`
- 如果 skill 找不到，先检查软链接是否还在：iCloud 同步、或在 Windows 上克隆时不一定保留软链接。在仓库根目录运行 `ln -sfn ../.agents/skills .claude/skills` 即可重建。新增或修改 skill 一律在 `.agents/skills/` 下进行
- 开工简报由 SessionStart hook 自动注入（`.claude/settings.json` 调用 `.agents/scripts/session_brief.py`）；收工时 Stop hook 会检查：会话改了仓库却没写记忆，就提醒一次
- 子目录里的 `CLAUDE.md` 也只是 `@AGENTS.md` 引用桩，规则写在同目录的 `AGENTS.md` 里
