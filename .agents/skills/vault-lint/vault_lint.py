#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""
vault-lint: deterministic checks of note frontmatter against the slot contracts
and 00-系统/Frontmatter 规范.md. No LLM involved; the vault-lint skill reads the
output and decides fixes.

The type registry, status enum and business-status enums are parsed from the
Frontmatter 规范 at run time, so that document stays the single source of truth.

Usage (from the vault root):
    python3 .agents/skills/vault-lint/vault_lint.py            # errors + warnings
    python3 .agents/skills/vault-lint/vault_lint.py --level info
    python3 .agents/skills/vault-lint/vault_lint.py --json
    python3 .agents/skills/vault-lint/vault_lint.py --path 04-资源
    uv run .agents/skills/vault-lint/vault_lint.py                      # if PyYAML is missing

Exit code: 1 if any error-level finding, else 0.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    sys.exit("vault-lint: PyYAML missing. Run with python3 or `uv run`.")

SPEC = "00-系统/Frontmatter 规范.md"
SKIP_TOP = {"00-系统", "90-附件"}          # not content slots
EXTRA_ROOTS = ["00-系统/agent-memory"]     # checked despite living under 00-系统
MEMORY_NOW = "00-系统/agent-memory/now.md"  # holds path claims in frontmatter
SKIP_DIRS = {".git", ".obsidian", ".trash", ".claude", ".agents", "node_modules"}
NON_NOTES = {"CLAUDE.md", "AGENTS.md"}      # agent instructions, not notes
README_RE = re.compile(r"^(?:.+-)?README\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LIFECYCLES = {"transient", "active", "durable", "frozen"}
REQUIRED = ("title", "type", "created", "updated", "tags")
LEGACY_WARN = ("ai_source",)
LEGACY_INFO = ("source", "source_repo", "source_commit", "url")
LEVELS = {"error": 0, "warn": 1, "info": 2}
# 有固定格式的敏感信息（见 Frontmatter 规范的 visibility）。故意收紧，避免代码示例里的 password = "pass" 误报
SENSITIVE = {
    "证件号": re.compile(r"(?<![\d])\d{6}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?![\d])"),
    "手机号": re.compile(r"(?<![\d])1[3-9]\d{9}(?![\d])"),
    "密码": re.compile(r"(?:密码|口令)\s*[：:]\s*\S{3,}"),
    "密钥": re.compile(r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{32,}|ghp_[A-Za-z0-9]{36,}|AKIA[0-9A-Z]{16}|xox[bp]-[A-Za-z0-9-]{20,})"),
}
PUBLIC, PRIVATE = "🌐 可公开", "🔒 私有"

# ---------------------------------------------------------------- spec parsing

def _section(text, heading_prefix):
    """Lines of the ### section whose heading starts with heading_prefix."""
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("### ") or line.startswith("## "):
            if inside:
                break
            inside = line.startswith(heading_prefix)
            continue
        if inside:
            out.append(line)
    return out


def load_spec(root):
    text = open(os.path.join(root, SPEC), encoding="utf-8").read()
    types = set()
    for line in _section(text, "### `type`"):
        cells = line.split("|")
        if line.startswith("|") and len(cells) > 3 and "---" not in line:
            types.update(re.findall(r"`([^`]+)`", cells[2]))
    statuses = set(re.findall(r"^- `([a-z]+)`", "\n".join(_section(text, "### `status`")), re.M))
    business = {}
    for line in _section(text, "### 业务状态"):
        cells = line.split("|")
        if line.startswith("|") and len(cells) > 4:
            field = re.findall(r"`([^`]+)`", cells[1])
            if field:
                business[field[0]] = set(re.findall(r"`([^`]+)`", cells[3]))
    if not types or not statuses or not business:
        sys.exit("vault-lint: could not parse type/status/business tables from %s" % SPEC)
    return types, statuses, business

# ---------------------------------------------------------------- helpers

def read_frontmatter(path):
    """Return (dict|None, body, error)."""
    try:
        raw = open(path, encoding="utf-8-sig").read()
    except UnicodeDecodeError:
        return None, "", "not UTF-8"
    raw = raw.replace("\r\n", "\n")
    if not raw.startswith("---\n"):
        return None, raw, None
    end = raw.find("\n---", 4)
    if end == -1:
        return None, raw, "frontmatter not closed"
    try:
        data = yaml.safe_load(raw[4:end]) or {}
    except yaml.YAMLError as e:
        return None, raw[end + 4:], "YAML: %s" % str(e).splitlines()[0]
    if not isinstance(data, dict):
        return None, raw[end + 4:], "frontmatter is not a mapping"
    return data, raw[end + 4:], None


def read_slot(dirpath):
    """Slot contract declared by this directory's README, or None."""
    for name in sorted(os.listdir(dirpath)):
        if README_RE.match(name):
            fm, _, _ = read_frontmatter(os.path.join(dirpath, name))
            if fm and isinstance(fm.get("slot"), dict):
                return dict(fm["slot"], _readme=os.path.join(dirpath, name))
    return None


def as_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str) and DATE_RE.match(v.strip()):
        return dt.date.fromisoformat(v.strip())
    return None


CODE_FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")
WIKILINK = re.compile(r"!?\[\[([^\]\|#\^\\]*)(?:[#\^][^\]\|]*)?(?:\\?\|[^\]]*)?\]\]")


def wikilinks(body):
    body = INLINE_CODE.sub("", CODE_FENCE.sub("", body))
    for m in WIKILINK.finditer(body):
        t = m.group(1).strip()
        if t and "{{" not in t and "<%" not in t:
            yield t


class LinkIndex(object):
    def __init__(self, root):
        self.names, self.paths, self.dirs = set(), set(), set()
        for d, ds, fs in os.walk(root):
            ds[:] = [x for x in ds if x not in SKIP_DIRS]
            self.dirs.update(x.casefold() for x in ds)
            for f in fs:
                rel = os.path.relpath(os.path.join(d, f), root).casefold()
                self.paths.add(rel)
                self.names.add(f.casefold())
                if f.endswith(".md"):
                    self.paths.add(rel[:-3])
                    self.names.add(f[:-3].casefold())

    def resolves(self, target, note_dir):
        t = unquote(target).casefold().strip()
        if t.startswith("./") or t.startswith("../"):
            t = os.path.normpath(os.path.join(note_dir.casefold(), t))
            return t in self.paths
        t = t.strip("/")
        if "/" not in t:
            return t in self.names or t + ".md" in self.names
        if t in self.paths:
            return True
        suffix = "/" + t
        return any(p.endswith(suffix) for p in self.paths)


CALENDAR_LINK = re.compile(r"(?:^|/)\d{4}-(?:\d{2}-\d{2}|W\d{2}|\d{2})$")


def link_kind(target, dirs):
    """'skip' for calendar navigation, 'path' for folder paths / relative links /
    attachments, 'wanted' for bare note names (Obsidian's not-yet-written notes)."""
    t = unquote(target).strip()
    if CALENDAR_LINK.search(t):
        return "skip"
    if re.search(r"\.[A-Za-z0-9]{2,5}$", t) and not t.lower().endswith(".md"):
        return "path"
    if t.startswith("./") or t.startswith("../"):
        return "path"
    if "/" in t and t.split("/")[0].casefold() in dirs:
        return "path"
    return "wanted"

# ---------------------------------------------------------------- lint

def lint(root, only_path=None):
    types, statuses, business = load_spec(root)
    today = dt.date.today()
    skills = set(os.listdir(os.path.join(root, ".agents", "skills")))
    links = LinkIndex(root)
    findings, slots, notes = [], 0, 0

    def add(sev, rule, path, detail=""):
        findings.append({"severity": sev, "rule": rule, "path": path, "detail": detail})

    tops = [x for x in sorted(os.listdir(root))
            if re.match(r"^\d\d-", x) and x not in SKIP_TOP and os.path.isdir(os.path.join(root, x))]
    tops += [x for x in EXTRA_ROOTS if os.path.isdir(os.path.join(root, x))]
    check_claims(root, add)
    for top in tops:
        effective = {}
        for d, ds, fs in os.walk(os.path.join(root, top)):
            ds[:] = sorted(x for x in ds if x not in SKIP_DIRS and not x.startswith("."))
            rel_d = os.path.relpath(d, root)
            own = read_slot(d)
            if own:
                slots += 1
                check_slot(own, rel_d, types, skills, add)
            slot = own or effective.get(os.path.dirname(d))
            effective[d] = slot
            if only_path and not (rel_d + "/").startswith(only_path.rstrip("/") + "/"):
                continue
            if slot and slot.get("lifecycle") == "frozen":
                continue
            for f in sorted(fs):
                if not f.endswith(".md") or f in NON_NOTES:
                    continue
                notes += 1
                check_note(os.path.join(d, f), os.path.relpath(os.path.join(d, f), root),
                           README_RE.match(f) is not None, slot, types, statuses,
                           business, links, today, add)
    return findings, slots, notes


def check_claims(root, add):
    """Path claims in agent-memory/now.md: each needs path/by/until; expired ones warn."""
    p = os.path.join(root, MEMORY_NOW)
    if not os.path.exists(p):
        return
    fm, _, err = read_frontmatter(p)
    claims = (fm or {}).get("claims") or []
    now = dt.datetime.now(dt.timezone.utc)
    for c in claims:
        if not isinstance(c, dict) or not all(c.get(k) for k in ("path", "by", "until")):
            add("error", "CLAIM_INVALID", MEMORY_NOW, "占用声明缺 path/by/until: %r" % (c,))
            continue
        until = c["until"]
        if isinstance(until, str):
            try:
                until = dt.datetime.fromisoformat(until)
            except ValueError:
                add("error", "CLAIM_INVALID", MEMORY_NOW, "until 不是 ISO 时间: %r" % c["until"])
                continue
        if isinstance(until, dt.datetime):
            if until.tzinfo is None:
                until = until.astimezone()
            if until < now:
                add("warn", "CLAIM_EXPIRED", MEMORY_NOW, "%s 对 %s 的占用已于 %s 过期" % (c["by"], c["path"], c["until"]))


def check_slot(slot, rel_d, types, skills, add):
    where = os.path.join(rel_d, os.path.basename(slot["_readme"]))
    acc = slot.get("accepts")
    if not isinstance(acc, list) or not acc:
        add("error", "SLOT_INVALID", where, "accepts 缺失或不是列表")
    else:
        bad = [a for a in acc if a != "*" and a not in types]
        if bad:
            add("error", "SLOT_INVALID", where, "accepts 含未登记的 type: %s" % ", ".join(map(str, bad)))
    lc = slot.get("lifecycle")
    if lc not in LIFECYCLES:
        add("error", "SLOT_INVALID", where, "lifecycle 非法: %r" % lc)
    age = slot.get("max_age_days")
    if lc == "transient" and not isinstance(age, int):
        add("error", "SLOT_INVALID", where, "transient 槽位需要整数 max_age_days")
    if age is not None and lc != "transient":
        add("warn", "SLOT_INVALID", where, "max_age_days 只对 transient 生效")
    owner = slot.get("owner")
    if owner and owner not in skills:
        add("info", "SLOT_OWNER_MISSING", where, "owner skill 尚不存在: %s" % owner)


def check_note(path, rel, is_readme, slot, types, statuses, business, links, today, add):
    fm, body, err = read_frontmatter(path)
    if err:
        add("error", "FM_PARSE", rel, err)
        return
    if fm is None:
        add("error", "TYPE_MISSING", rel, "没有 frontmatter")
        fm = {}
    t = fm.get("type")
    if fm and t is None:
        add("error", "TYPE_MISSING", rel, "没有 type 字段")
    elif t is not None and (not isinstance(t, str) or t not in types):
        add("error", "TYPE_UNKNOWN", rel, "type 未在规范登记: %r" % (t,))
    elif t and slot and not is_readme and t != "README":
        acc = slot.get("accepts") or []
        if "*" not in acc and t not in acc:
            add("error", "TYPE_NOT_IN_SLOT", rel, "%s 不在槽位 accepts %s" % (t, acc))

    if fm:
        missing = [k for k in REQUIRED if k != "type" and k not in fm]
        if missing:
            add("info", "FIELD_MISSING", rel, ", ".join(missing))
        st = fm.get("status")
        if st is not None and st not in statuses:
            add("warn", "STATUS_LEGACY", rel, "status=%r（应为 %s，旧业务含义迁到独立字段）" % (st, "/".join(sorted(statuses))))
        for field, allowed in business.items():
            v = fm.get(field)
            if v is not None and v not in allowed:
                add("error", "BUSINESS_ENUM", rel, "%s=%r 不在 %s" % (field, v, "/".join(sorted(allowed))))
        for k in ("created", "updated"):
            v = fm.get(k)
            if v is not None and (isinstance(v, dt.datetime) or as_date(v) is None):
                add("warn", "DATE_FORMAT", rel, "%s=%r 应为 YYYY-MM-DD" % (k, v))
        for k in LEGACY_WARN:
            if k in fm:
                add("warn", "LEGACY_FIELD", rel, "%s → generated.by" % k)
        for k in LEGACY_INFO:
            if k in fm:
                add("info", "LEGACY_FIELD", rel, "%s → sources[].resource" % k)

    kinds = sorted(k for k, r in SENSITIVE.items() if r.search(open(path, encoding="utf-8").read()))
    vis = str((fm or {}).get("visibility") or "")
    if kinds and PUBLIC in vis:
        add("error", "PRIVACY_PUBLIC", rel, "标了可公开，但含%s" % "、".join(kinds))
    elif kinds and PRIVATE not in vis:
        add("warn", "SENSITIVE_UNMARKED", rel, "含%s，应显式标 visibility: \"%s\"" % ("、".join(kinds), PRIVATE))

    if slot and not is_readme:
        lc = slot.get("lifecycle")
        if lc == "transient" and isinstance(slot.get("max_age_days"), int):
            born = as_date(fm.get("created")) or dt.date.fromtimestamp(os.path.getmtime(path))
            days = (today - born).days
            if days > slot["max_age_days"]:
                add("warn", "TRANSIENT_AGE", rel, "已停留 %d 天（上限 %d）" % (days, slot["max_age_days"]))
        if lc == "active" and fm.get("project_status") in ("completed", "cancelled"):
            add("warn", "ACTIVE_DONE", rel, "project_status=%s，应归档" % fm.get("project_status"))

    note_dir = os.path.dirname(rel)
    for l in sorted(set(wikilinks(body))):
        kind = link_kind(l, links.dirs)
        if kind == "skip" or links.resolves(l, note_dir):
            continue
        if kind == "path":
            add("warn", "DEAD_LINK", rel, "[[%s]]" % l)
        else:
            add("info", "WANTED_NOTE", rel, "[[%s]]（笔记尚不存在）" % l)

# ---------------------------------------------------------------- output

def report(findings, slots, notes, level, limit):
    cnt = Counter(f["severity"] for f in findings)
    print("vault-lint: %d 篇笔记，%d 份槽位契约 — %d error，%d warn，%d info"
          % (notes, slots, cnt["error"], cnt["warn"], cnt["info"]))
    by_rule = defaultdict(list)
    for f in findings:
        by_rule[(LEVELS[f["severity"]], f["severity"], f["rule"])].append(f)
    for (_, sev, rule), items in sorted(by_rule.items()):
        if LEVELS[sev] > LEVELS[level]:
            continue
        print("\n[%s] %s (%d)" % (sev, rule, len(items)))
        by_dir = defaultdict(list)
        for f in items:
            by_dir[os.path.dirname(f["path"])].append(f)
        for d, fs in sorted(by_dir.items(), key=lambda x: -len(x[1])):
            print("  %s (%d)" % (d, len(fs)))
            for f in fs[:limit]:
                print("    - %s  %s" % (os.path.basename(f["path"]), f["detail"]))
            if len(fs) > limit:
                print("    … 另有 %d 条（--limit 0 显示全部）" % (len(fs) - limit))
    hidden = {r: len(v) for (_, s, r), v in by_rule.items() if LEVELS[s] > LEVELS[level]}
    if hidden:
        print("\n未展开（--level info 查看）：" + "，".join("%s %d" % kv for kv in sorted(hidden.items())))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=".", help="vault 根目录（默认当前目录）")
    ap.add_argument("--path", help="只检查该相对路径下的笔记（契约继承仍按全库计算）")
    ap.add_argument("--level", choices=list(LEVELS), default="warn", help="展开明细的最低级别")
    ap.add_argument("--limit", type=int, default=8, help="每个目录最多列出几条，0 表示不限")
    ap.add_argument("--json", action="store_true", help="输出 JSON（供 skill 解析）")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.exists(os.path.join(root, SPEC)):
        sys.exit("vault-lint: %s 不是 vault 根目录（找不到 %s）" % (root, SPEC))
    findings, slots, notes = lint(root, a.path)
    if a.json:
        json.dump({"notes": notes, "slots": slots, "findings": findings}, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        report(findings, slots, notes, a.level, a.limit or 10 ** 9)
    sys.exit(1 if any(f["severity"] == "error" for f in findings) else 0)


if __name__ == "__main__":
    main()
