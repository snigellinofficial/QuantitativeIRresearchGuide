# -*- coding: utf-8 -*-
"""vault-v2 复核脚本。

检查项共八类，依次为卡片数、frontmatter 与题录一致、七节标题、
关联双向闭合、矩阵行数与列数、阶梯覆盖与交叉计数、index.json 可解析、
写作规范（单句长度、空格、标点、禁用词）。
"""

import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT = os.path.join(ROOT, "vault-v2")
CATALOG = os.path.join(ROOT, "catalog-v2.json")

SECTIONS = [
    "## 一句话概括",
    "## 研究设计",
    "## 数据结构",
    "## 可迁移的做法",
    "## 主要结论",
    "## 复制这项研究需要注意",
    "## 关联文献",
]

FIELDS = [
    "id", "topic", "short", "authors", "year", "title", "venue", "volume",
    "doi", "cites", "difficulty", "data_kind", "design", "unit", "tags",
]

STR_FIELDS = ["short", "authors", "title", "venue", "volume", "doi", "data_kind", "design", "unit"]
INT_FIELDS = ["year", "cites", "difficulty"]

CATEGORIES = ["数据形态相同", "识别逻辑相同", "互为稳健性检验"]

LINK_RE = re.compile(r"^- \[\[([^\]]+)\]\] (.+)$")
ID_RE = re.compile(r"^([A-Z]\d{2})-")
HEAD_RE = re.compile(r"^## ")

BANNED = ["进行", "——", "下面", "接下来", "综上", "总而言之", "值得注意"]

MAX_SENT = 40

errors = []
warns = []


def fail(msg):
    errors.append(msg)


def cjk(ch):
    return "\u4e00" <= ch <= "\u9fff"


def visible_len(text):
    """按汉字与英文词计数的句长，空格不计。"""
    total = 0
    word = False
    for ch in text:
        if ch == " ":
            word = False
            continue
        if cjk(ch):
            total += 1
            word = False
        elif ch.isascii() and (ch.isalnum()):
            if not word:
                total += 1
                word = True
        else:
            total += 1
            word = False
    return total


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def split_front(text, path):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        fail("%s 缺 frontmatter 起始行" % path)
        return {}, lines, 0
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        fail("%s 缺 frontmatter 结束行" % path)
        return {}, lines, 0
    meta = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            fail("%s frontmatter 行无法解析 %r" % (path, line))
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, lines, end


def parse_scalar(value):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    return value


def check_notes(cat, order):
    notes_dir = os.path.join(VAULT, "notes")
    files = sorted(os.listdir(notes_dir))
    if len(files) != 100:
        fail("卡片数 %d，应为 100" % len(files))
    links = {}
    for fname in files:
        if not fname.endswith(".md"):
            fail("notes 目录含非卡片文件 %s" % fname)
            continue
        path = os.path.join(notes_dir, fname)
        text = read(path)
        meta, lines, end = split_front(text, fname)

        for field in FIELDS:
            if field not in meta:
                fail("%s 缺字段 %s" % (fname, field))

        pid = parse_scalar(meta.get("id", ""))
        if pid not in cat:
            fail("%s 的 id %r 不在题录中" % (fname, pid))
            continue
        c = cat[pid]
        if fname != "%s-%s.md" % (pid, c["_surname"]):
            fail("%s 文件名与编号姓氏不符" % fname)
        if parse_scalar(meta.get("topic", "")) != c["topic"]:
            fail("%s 的 topic 与题录不符" % fname)
        for field in STR_FIELDS:
            got = parse_scalar(meta.get(field, ""))
            if got != c[field]:
                fail("%s 的 %s 与题录不符：%r != %r" % (fname, field, got, c[field]))
        for field in INT_FIELDS:
            got = meta.get(field, "").strip()
            if not got.isdigit() or int(got) != c[field]:
                fail("%s 的 %s 与题录不符：%r" % (fname, field, got))

        tags_line = meta.get("tags", "")
        if not (tags_line.startswith("[") and tags_line.endswith("]")):
            fail("%s 的 tags 不是列表" % fname)
        else:
            tags = [t.strip() for t in tags_line[1:-1].split(",") if t.strip()]
            if not 3 <= len(tags) <= 5:
                fail("%s 的 tags 数量 %d" % (fname, len(tags)))

        body = lines[end + 1:]
        heads = [ln.strip() for ln in body if HEAD_RE.match(ln)]
        if heads != SECTIONS:
            fail("%s 的七节标题不符：%s" % (fname, heads))

        design_heads = ["- **观测单元**", "- **处理变量**", "- **结果变量**", "- **识别逻辑**"]
        got_heads = [ln.split("**")[1] for ln in body if ln.startswith("- **")]
        if got_heads != [h.strip("- *") for h in design_heads]:
            fail("%s 研究设计四条标签不符：%s" % (fname, got_heads))

        filled = {}
        current = None
        for ln in body:
            if HEAD_RE.match(ln):
                current = ln.strip()
                filled[current] = 0
                continue
            if current and ln.strip():
                filled[current] += 1
        for sec in SECTIONS:
            if filled.get(sec, 0) == 0:
                fail("%s 的 %s 一节为空" % (fname, sec))

        link_rows = []
        in_links = False
        for ln in body:
            if ln.strip() == "## 关联文献":
                in_links = True
                continue
            if in_links and ln.startswith("## "):
                in_links = False
            if not in_links:
                continue
            if not ln.startswith("- "):
                continue
            match = LINK_RE.match(ln)
            if not match:
                fail("%s 关联行格式不符：%r" % (fname, ln))
                continue
            target, reason = match.group(1), match.group(2)
            tid = target.split("-")[0]
            if tid not in cat:
                fail("%s 关联目标 %r 不在题录中" % (fname, target))
                continue
            if target != "%s-%s" % (tid, cat[tid]["_surname"]):
                fail("%s 关联目标文件名不符 %r" % (fname, target))
            if not reason.startswith("因为"):
                fail("%s 关联理由未以因为开头 %r" % (fname, ln))
            if not any(reason.startswith("因为" + cg) for cg in CATEGORIES):
                fail("%s 关联理由未落在三类 %r" % (fname, ln))
            link_rows.append((tid, reason))
        if not 3 <= len(link_rows) <= 5:
            fail("%s 关联数 %d 越界" % (fname, len(link_rows)))
        if len(set(t for t, _r in link_rows)) != len(link_rows):
            fail("%s 关联目标重复" % fname)
        links[pid] = link_rows

        # 主要结论不得出现题录之外的数字
        sec = None
        for ln in body:
            if HEAD_RE.match(ln):
                sec = ln.strip()
                continue
            if sec != "## 主要结论":
                continue
            for num in re.findall(r"\d+", ln):
                if num not in json.dumps(c, ensure_ascii=False):
                    fail("%s 主要结论出现题录外的数字 %s" % (fname, num))
    return links


def check_reciprocal(links, cat):
    total = 0
    for pid, rows in links.items():
        for target, reason in rows:
            total += 1
            back = links.get(target, [])
            hit = [r for t, r in back if t == pid]
            if not hit:
                fail("%s 指向 %s 的关联未回指" % (pid, target))
                continue
            for catg in CATEGORIES:
                a = reason.startswith("因为" + catg)
                b = hit[0].startswith("因为" + catg)
                if a != b:
                    fail("%s 与 %s 的关联归类不一致" % (pid, target))
                    break
    if total % 2 != 0:
        fail("关联总数 %d 为奇数，双向必不闭合" % total)
    return total


def check_matrix(cat, order):
    text = read(os.path.join(VAULT, "matrix.md"))
    header = "| 编号 | 简称 | 专题 | 难度 | 观测单元 | 识别策略 | 数据形态 | 期刊 | 年份 |"
    if header not in text:
        fail("matrix 表头不符")
    rows = []
    started = False
    for line in text.split("\n"):
        if line.strip() == header:
            started = True
            continue
        if started:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("- :"):
                continue
            rows.append(cells)
    if len(rows) != 100:
        fail("matrix 行数 %d，应为 100" % len(rows))
    for cells in rows:
        if len(cells) != 9:
            fail("matrix 行列数 %d：%s" % (len(cells), cells[0]))
            continue
        if cells[3] not in "12345" or len(cells[3]) != 1:
            fail("matrix 难度取值越界 %s %s" % (cells[0], cells[3]))
        pid = cells[0]
        if pid in cat:
            c = cat[pid]
            if cells[1] != c["short"] or cells[2] != c["topic"]:
                fail("matrix 行与题录不符 %s" % pid)
            if int(cells[3]) != c["difficulty"] or cells[4] != c["unit"]:
                fail("matrix 难度或单元不符 %s" % pid)
            if cells[5] != c["design"] or cells[6] != c["data_kind"] or cells[7] != c["venue"]:
                fail("matrix 方法或数据或期刊不符 %s" % pid)
            if str(c["year"]) != cells[8]:
                fail("matrix 年份不符 %s" % pid)
        else:
            fail("matrix 出现未知编号 %s" % pid)
    ids = [r[0] for r in rows]
    if sorted(ids) != sorted(order):
        fail("matrix 编号集合与题录不一致")
    return len(rows)


def check_ladder(cat, order, topics):
    text = read(os.path.join(VAULT, "ladder.md"))
    seen = []
    for line in text.split("\n"):
        m = re.match(r"^- ([A-Z]\d{2}) (.+?)：(.+)$", line)
        if m:
            seen.append(m.group(1))
    if len(seen) != 100:
        fail("ladder 文献行 %d，应为 100" % len(seen))
    if len(set(seen)) != len(seen):
        fail("ladder 有重复编号")
    if sorted(set(seen)) != sorted(order):
        fail("ladder 编号集合与题录不一致")
    for line in text.split("\n"):
        m = re.match(r"^- ([A-Z]\d{2}) ", line)
        if not m:
            continue
        pid = m.group(1)
        if pid in cat and visible_len(line[2:]) > MAX_SENT:
            fails = visible_len(line[2:])
            fail("ladder 行过长 %d %s" % (fails, pid))

    # 交叉计数表
    rows = {}
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7 or not re.match(r"^[A-Z] ", cells[0]):
            continue
        rows[cells[0][0]] = [int(x) for x in cells[1:]]
    if len(rows) != len(topics):
        fail("ladder 交叉表行数 %d" % len(rows))
    for t in topics:
        tid = t["id"]
        expect = [0] * 6
        for pid in order:
            if cat[pid]["topic"] == tid:
                expect[cat[pid]["difficulty"] - 1] += 1
                expect[5] += 1
        if rows.get(tid) != expect:
            fail("ladder 交叉表 %s 与题录不符 %s != %s" % (tid, rows.get(tid), expect))


def check_index_json(cat, order, topics, links):
    payload = json.loads(read(os.path.join(VAULT, "index.json")))
    if payload.get("generated") != "2026-10-29":
        fail("index.json generated 字段不符")
    if len(payload.get("papers", [])) != 100:
        fail("index.json papers 数量不符")
    ids = [p["id"] for p in payload.get("papers", [])]
    if sorted(ids) != sorted(order):
        fail("index.json 编号集合与题录不一致")
    for p in payload["papers"]:
        c = cat[p["id"]]
        if p["short"] != c["short"] or p["topic"] != c["topic"]:
            fail("index.json 条目与题录不符 %s" % p["id"])
        if p["difficulty"] != c["difficulty"] or p["year"] != c["year"]:
            fail("index.json 难度或年份不符 %s" % p["id"])
        if p["venue"] != c["venue"]:
            fail("index.json 期刊不符 %s" % p["id"])
        note = os.path.join(VAULT, p["note"].replace("/", os.sep))
        if not os.path.exists(note):
            fail("index.json 卡片路径不存在 %s" % p["note"])
        if sorted(p["links"]) != sorted(t for t, _r in links.get(p["id"], [])):
            fail("index.json 关联与卡片不符 %s" % p["id"])
        for other in p["links"]:
            if p["id"] not in [q["links"] for q in payload["papers"] if q["id"] == other][0]:
                fail("index.json 关联未闭合 %s-%s" % (p["id"], other))
    tsum = 0
    for t in payload.get("topics", []):
        tsum += t["count"]
        real = len([pid for pid in order if cat[pid]["topic"] == t["id"]])
        if t["count"] != real:
            fail("index.json 专题计数不符 %s" % t["id"])
        if not os.path.exists(os.path.join(VAULT, t["file"])):
            fail("index.json 专题文件不存在 %s" % t["file"])
    if tsum != 100:
        fail("index.json 专题计数合计 %d" % tsum)
    if len(payload.get("difficulty_legend", {})) != 5:
        fail("index.json 难度定义条数不符")


def prose_part(line):
    """去掉编号与标签前缀，只留散文部分。"""
    m = re.match(r"^- \[\[[^\]]+\]\] (.+)$", line)
    if m:
        return m.group(1)
    m = re.match(r"^- \*\*[^*]+\*\* (.+)$", line)
    if m:
        return m.group(1)
    m = re.match(r"^- ([A-Z]\d{2}) .+?：(.+)$", line)
    if m:
        return m.group(2)
    return line


def is_emoji(ch):
    code = ord(ch)
    return (0x1F300 <= code <= 0x1FAFF) or (0x2600 <= code <= 0x27BF) or \
        (0x1F000 <= code <= 0x1F0FF) or code == 0xFE0F


def check_prose():
    md_files = [os.path.join(VAULT, n) for n in sorted(os.listdir(VAULT)) if n.endswith(".md")]
    md_files += [os.path.join(VAULT, "notes", n)
                 for n in sorted(os.listdir(os.path.join(VAULT, "notes")))]
    long_sents = []
    space_hits = []
    punct_hits = []
    banned_hits = []
    for path in md_files:
        text = read(path)
        rel = os.path.relpath(path, VAULT)
        lines = text.split("\n")
        start = 0
        if lines and lines[0].strip() == "---":
            for idx in range(1, len(lines)):
                if lines[idx].strip() == "---":
                    start = idx + 1
                    break
        for line in lines[start:]:
            stripped = line.strip()
            if not stripped or stripped.startswith("|") or stripped.startswith("#"):
                continue
            if stripped.startswith("```"):
                continue
            for word in BANNED:
                if word in stripped:
                    banned_hits.append((rel, word, stripped[:40]))
            for ch in stripped:
                if is_emoji(ch):
                    banned_hits.append((rel, "emoji", stripped[:40]))
                    break
            subject = prose_part(stripped)
            for frag in re.split(r"[。！？]", subject):
                frag = frag.strip()
                if not frag:
                    continue
                if visible_len(frag) > MAX_SENT:
                    long_sents.append((rel, visible_len(frag), frag))
            for i, ch in enumerate(stripped[:-1]):
                nxt = stripped[i + 1]
                if (cjk(ch) and nxt.isascii() and (nxt.isalnum())) or \
                        (ch.isascii() and ch.isalnum() and cjk(nxt)):
                    space_hits.append((rel, stripped[max(0, i - 6):i + 7]))
                    break
            for ch in [",", ";", ":", "(", ")", "!", "?"]:
                for m in re.finditer(re.escape(ch), stripped):
                    before = stripped[m.start() - 1] if m.start() else ""
                    after = stripped[m.start() + 1] if m.start() + 1 < len(stripped) else ""
                    if (before and cjk(before)) or (after and cjk(after)):
                        punct_hits.append((rel, ch, stripped[max(0, m.start() - 8):m.start() + 8]))
                        break
    for rel, n, frag in long_sents:
        fail("单句 %d 字：%s | %s" % (n, rel, frag))
    for rel, frag in space_hits:
        fail("汉字与半角字母数字缺空格：%s | %s" % (rel, frag))
    for rel, ch, frag in punct_hits:
        fail("半角标点紧邻汉字：%s | %s | %s" % (rel, ch, frag))
    for rel, word, frag in banned_hits:
        fail("禁用词 %s：%s | %s" % (word, rel, frag))


def main():
    with open(CATALOG, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    cat = {}
    for p in data["papers"]:
        cat[p["id"]] = dict(p)
        cat[p["id"]]["_surname"] = ""
    order = [p["id"] for p in data["papers"]]
    topics = data["topics"]

    # 姓氏由文件名反推，避免重复维护
    notes_dir = os.path.join(VAULT, "notes")
    for fname in os.listdir(notes_dir):
        m = ID_RE.match(fname)
        if m and m.group(1) in cat:
            cat[m.group(1)]["_surname"] = fname.split("-", 1)[1][:-3]

    links = check_notes(cat, order)
    total = check_reciprocal(links, cat)
    n_matrix = check_matrix(cat, order)
    check_ladder(cat, order, topics)
    check_index_json(cat, order, topics, links)
    check_prose()

    readme_lines = len(read(os.path.join(VAULT, "README.md")).rstrip("\n").split("\n"))
    if readme_lines > 40:
        fail("README 行数 %d 超过 40" % readme_lines)

    print("卡片 %d 张" % len(links))
    print("关联 %d 条，双向闭合检查完毕" % total)
    print("矩阵 %d 行" % n_matrix)
    print("README %d 行" % readme_lines)
    if errors:
        print("问题 %d 项" % len(errors))
        for e in errors[:60]:
            print("  -", e)
        sys.exit(1)
    print("全部检查通过")


if __name__ == "__main__":
    main()
