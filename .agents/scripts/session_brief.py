#!/usr/bin/env python3
"""
开工简报：把共享记忆（交接板、用户画像、经验）和仓库状态汇总成一段文字。

任何 agent 开工时都可以运行它，代替逐个读文件：
    python3 .agents/scripts/session_brief.py

Claude Code 通过 SessionStart hook 调用（--hook）：stdout 会注入会话上下文，
同时记下本次会话开始时的仓库状态，供收工检查 session_end_check.py 比对。
"""

import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MEM = os.path.join(ROOT, "00-系统", "agent-memory")
MUST_READ = [("交接板", "now.md"), ("用户画像", "profile.md"), ("经验与陷阱", "lessons.md")]


def git(*args):
    r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    return r.stdout.strip()


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else ("", text)


def active_claims(fm_text):
    if re.search(r"^claims:[ \t]*\[[ \t]*\][ \t]*$", fm_text, re.M) or "claims:" not in fm_text:
        return []                                   # 没有声明：不依赖 PyYAML 也能判断
    try:
        import yaml
        claims = (yaml.safe_load(fm_text) or {}).get("claims") or []
    except ImportError:
        return ["（有占用声明，但缺 PyYAML 无法解析，请直接查看 now.md）"]
    except Exception:
        return ["（claims 解析失败，请直接查看 now.md）"]
    now = dt.datetime.now(dt.timezone.utc)
    out = []
    for c in claims:
        until = c.get("until") if isinstance(c, dict) else None
        if isinstance(until, str):
            try:
                until = dt.datetime.fromisoformat(until)
            except ValueError:
                until = None
        if isinstance(until, dt.datetime) and until.tzinfo is None:
            until = until.astimezone()
        state = "已过期，可接手" if until and until < now else "有效"
        out.append("%s 占用 %s，到 %s（%s）：%s" % (c.get("by"), c.get("path"), c.get("until"), state, c.get("why", "")))
    return out


def body_of(name):
    fm, body = split_frontmatter(open(os.path.join(MEM, name), encoding="utf-8").read())
    body = re.sub(r"^# .*\n", "", body.strip(), count=1)          # 去掉一级标题
    return fm, re.sub(r"\n{3,}", "\n\n", body).strip()


def brief():
    lines = ["# 开工简报（共享记忆 + 仓库状态，由 .agents/scripts/session_brief.py 生成）", ""]
    for title, name in MUST_READ:
        fm, body = body_of(name)
        lines += ["## %s（00-系统/agent-memory/%s）" % (title, name), body, ""]
        if name == "now.md":
            claims = active_claims(fm)
            lines += ["路径占用声明：" + ("；".join(claims) if claims else "无"), ""]
    dirty = [l for l in git("status", "--porcelain").splitlines() if l.strip()]
    lines += ["## 仓库状态"]
    if dirty:
        shown = "、".join(l[3:] for l in dirty[:8]) + ("……" if len(dirty) > 8 else "")
        lines.append("- 未提交改动 %d 处：%s。不是你做的就不要碰，也不要一起提交" % (len(dirty), shown))
    else:
        lines.append("- 工作区干净")
    recent = git("log", "--since=7.days", "--format=%h %s").splitlines()
    lines.append("- 近 7 天提交 %d 条，最近几条：" % len(recent))
    lines += ["  - " + r for r in recent[:6]]
    lines += ["", "需要代表用户判断或回答时，另读 00-系统/agent-memory/persona.md。收工协议见 AGENTS.md「共享记忆」。"]
    return "\n".join(lines)


def record_start(session_id):
    """记下会话开始时的仓库状态；resume/compact 时保留最早的一份。"""
    p = os.path.join(tempfile.gettempdir(), "agent-session-%s.json" % re.sub(r"[^\w-]", "_", session_id))
    if not os.path.exists(p):
        json.dump({"head": git("rev-parse", "HEAD"), "dirty": git("status", "--porcelain"),
                   "started": dt.datetime.now().timestamp()}, open(p, "w"))


if __name__ == "__main__":
    if "--hook" in sys.argv:
        try:
            data = json.load(sys.stdin)
        except Exception:
            data = {}
        if data.get("session_id"):
            record_start(data["session_id"])
    print(brief())
