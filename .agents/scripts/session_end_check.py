#!/usr/bin/env python3
"""
收工检查：本次会话改过仓库，却既没写会话记录、也没更新交接板时，提醒 agent 按收工协议补上。

Claude Code 通过 Stop hook 调用（--hook）。只和 session_brief.py 在开工时记下的状态比对，
所以会话开始前就存在的改动（比如别的 agent 留下的）不算。每个会话最多提醒一次，
agent 也可以说明"这次改动不值得记录"后直接结束，避免强迫写流水账。
"""

import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MEM = os.path.join(ROOT, "00-系统", "agent-memory")


def git(*args):
    r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    return r.stdout.strip()


def memory_touched_since(ts):
    paths = [os.path.join(MEM, "now.md")]
    sess = os.path.join(MEM, "sessions")
    paths += [os.path.join(sess, f) for f in os.listdir(sess) if f.endswith(".md")]
    return any(os.path.getmtime(p) > ts for p in paths if os.path.exists(p))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    sid = data.get("session_id")
    if not sid or data.get("stop_hook_active"):
        return
    key = re.sub(r"[^\w-]", "_", sid)
    start_p = os.path.join(tempfile.gettempdir(), "agent-session-%s.json" % key)
    done_p = os.path.join(tempfile.gettempdir(), "agent-session-%s.reminded" % key)
    if not os.path.exists(start_p) or os.path.exists(done_p):
        return
    start = json.load(open(start_p))
    changed = git("rev-parse", "HEAD") != start["head"] or git("status", "--porcelain") != start["dirty"]
    if not changed or memory_touched_since(start["started"]):
        return
    open(done_p, "w").close()
    print(json.dumps({"decision": "block", "reason": (
        "收工检查：这次会话改动了仓库，但还没按 AGENTS.md 的收工协议留下记忆。请："
        "1) 有实质改动或决策，就在 00-系统/agent-memory/sessions/ 写一篇会话记录；"
        "2) 更新 now.md：撤销自己的占用声明，增删待接手事项。"
        "如果这次只是很小的改动、不值得记录，简短说明理由后结束即可。")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
