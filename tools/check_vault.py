# -*- coding: utf-8 -*-
"""vault 结构与写作规范校验。"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT = os.path.join(ROOT, "vault")
CATALOG = os.path.join(ROOT, "catalog.json")

SECTIONS = [
    "## 一句话概括",
    "## 研究设计",
    "## 数据结构",
    "## 可迁移的做法",
    "## 主要结论",
    "## 复制这项研究需要注意",
    "## 关联文献",
]
FRONT_KEYS = ["id", "group", "short", "authors", "year", "title", "venue",
              "volume", "doi", "cites", "unit", "design", "tags"]
TREAT = {"二值政策", "连续暴露度", "价格冲击交互", "网络位置", "代理测量",
         "无处理变量（数据基础设施）"}
OUTCOME = {"行政统计", "遥感代理", "调查数据", "冲突事件记录", "网络整体结构"}
DATA_KIND = {"点", "线", "面", "栅格", "关系边", "混合"}
CATS = {"数据形态相同", "识别逻辑相同", "互为稳健性检验"}

CJK = r"\u4e00-\u9fff"
errors = []
warns = []


def err(msg):
    errors.append(msg)


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def split_front(text):
    assert text.startswith("---\n"), "缺少 frontmatter"
    body = text[4:]
    idx = body.index("\n---\n")
    return body[:idx], body[idx + 5:]


def prose_lines(text):
    """去掉 frontmatter、表格行、围栏代码块与行内代码后的正文行。"""
    out = []
    in_code = False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("|"):
            continue
        if line.startswith("#"):
            out.append(line)
            continue
        out.append(re.sub(r"`[^`]*`", "", line))
    return out


def check_writing(path, text):
    probe = text
    if probe.startswith("---\n"):
        _fm, body_text = split_front(probe)
        probe = body_text
    lines = []
    in_code = False
    for line in probe.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.startswith("|"):
            continue
        lines.append(re.sub(r"`[^`]*`", "", line))
    joined = "\n".join(lines)

    if "\u2014\u2014" in joined:
        err("%s 出现破折号" % path)
    if "——" in joined:
        err("%s 出现破折号" % path)
    if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]", joined):
        err("%s 出现 emoji" % path)
    for word in ["进行", "下面", "接下来", "让我们", "众所周知", "综上所述",
                 "总而言之", "值得注意", "首先我们", "本文认为"]:
        if word in joined:
            err("%s 出现禁用词 %s" % (path, word))
    if "..." in joined or "……" in joined:
        err("%s 省略号写法不合规" % path)

    for line in lines:
        for bad in [",", ";", "!", "?", "(", ")"]:
            if re.search(r"[%s]\s*\%s" % (CJK, bad), line):
                err("%s 中文语境半角标点 %r：%s" % (path, bad, line.strip()[:40]))
        for m in re.finditer(r"[%s][A-Za-z0-9]|[A-Za-z0-9][%s]" % (CJK, CJK), line):
            err("%s 中英之间缺空格：%s" % (path, m.group(0)))

    for line in lines:
        if not line.strip():
            continue
        stem = re.sub(r"\[\[[^\]]+\]\]", "", line.strip())
        stem = re.sub(r"^[-*\d.\s]+", "", stem)
        for sent in re.split(r"[。！？]", stem):
            n = len(re.findall(r"[%s]" % CJK, sent))
            if n > 40:
                err("%s 单句 %d 汉字：%s" % (path, n, sent.strip()[:50]))


def main():
    cat = json.loads(read(CATALOG))
    papers = {p["id"]: p for p in cat["papers"]}
    order = [p["id"] for p in cat["papers"]]

    expected = ["00-index.md", "matrix.md", "index.json", "README.md"]
    expected += ["01-group-A-断点与边界.md", "02-group-B-可达性与基础设施.md",
                 "03-group-C-电力与能源设施.md", "04-group-D-冲突资源与网格.md",
                 "05-group-E-网络与关系.md", "06-group-F-测量卫星与前沿.md"]
    notes = [f for f in os.listdir(os.path.join(VAULT, "notes")) if f.endswith(".md")] \
        if os.path.isdir(os.path.join(VAULT, "notes")) else []
    expected += ["notes/" + n for n in sorted(notes)]

    for rel in expected:
        if not os.path.isfile(os.path.join(VAULT, rel)):
            err("缺少文件 %s" % rel)
    if len(notes) != 26:
        err("卡片数 %d，应为 26" % len(notes))

    link_map = {}
    for pid in order:
        stem = [n for n in notes if n.startswith(pid + "-")]
        if len(stem) != 1:
            err("%s 卡片数异常" % pid)
            continue
        rel = os.path.join("notes", stem[0])
        text = read(os.path.join(VAULT, rel))
        fm, body = split_front(text)
        keys = {}
        for line in fm.split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                keys[k.strip()] = v.strip()
        for k in FRONT_KEYS:
            if k not in keys:
                err("%s frontmatter 缺 %s" % (rel, k))
        if keys.get("id") != pid:
            err("%s id 不符" % rel)
        if keys.get("group") != papers[pid]["group"]:
            err("%s group 不符" % rel)
        for fld in ["short", "authors", "title", "venue", "volume", "doi", "unit"]:
            if keys.get(fld, "").strip('"') != papers[pid][fld]:
                err("%s 字段 %s 与题录不符" % (rel, fld))
        if keys.get("year") != str(papers[pid]["year"]):
            err("%s year 不符" % rel)
        if keys.get("cites") != str(papers[pid]["cites"]):
            err("%s cites 不符" % rel)
        if not keys.get("tags", "").startswith("[") or keys["tags"].count(",") < 2:
            err("%s tags 数量不足" % rel)

        found = [ln for ln in body.split("\n") if ln.startswith("## ")]
        if found != SECTIONS:
            err("%s 小节标题或顺序不符：%s" % (rel, found))

        tail = body.split("## 关联文献", 1)[-1]
        targets = re.findall(r"\[\[([^\]]+)\]\]", tail)
        link_map[pid] = targets
        if not 3 <= len(targets) <= 5:
            err("%s 关联数 %d" % (rel, len(targets)))
        if len(set(targets)) != len(targets):
            err("%s 关联重复" % rel)
        for t in targets:
            if not os.path.isfile(os.path.join(VAULT, "notes", t + ".md")):
                err("%s 双链目标不存在 %s" % (rel, t))
        for line in [l for l in tail.split("\n") if l.startswith("- [[")]:
            m = re.match(r"- \[\[([^\]]+)\]\] 因为([^，]+)，", line)
            if not m:
                err("%s 关联行格式不符：%s" % (rel, line[:30]))
            elif m.group(2) not in CATS:
                err("%s 关联归类越界：%s" % (rel, m.group(2)))

    name_to_id = {}
    for pid in order:
        stem = [n for n in notes if n.startswith(pid + "-")][0][:-3]
        name_to_id[stem] = pid

    for pid, targets in link_map.items():
        back = []
        own = [n for n in notes if n.startswith(pid + "-")][0][:-3]
        for t in targets:
            tid = name_to_id.get(t)
            if tid is None:
                continue
            back.append(tid)
            if own not in link_map.get(tid, []):
                err("单向关联 %s -> %s" % (pid, tid))
        cross = [t for t in back if papers[t]["group"] != papers[pid]["group"]]
        same = [t for t in back if papers[t]["group"] == papers[pid]["group"]]
        if len(cross) > 2:
            err("%s 跨组 %d 条" % (pid, len(cross)))
        if not same:
            err("%s 无组内互链" % pid)

    matrix = read(os.path.join(VAULT, "matrix.md"))
    rows = [l for l in matrix.split("\n") if l.startswith("| ") and l.count("|") == 9]
    body_rows = [l for l in rows if re.match(r"\| [A-F]\d ", l)]
    if len(body_rows) != 26:
        err("matrix 数据行 %d，应为 26" % len(body_rows))
    for line in body_rows:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            err("matrix 列数 %d：%s" % (len(cells), line[:30]))
            continue
        if cells[4] not in TREAT:
            err("matrix 处理变量类型越界 %s：%s" % (cells[0], cells[4]))
        if cells[6] not in OUTCOME:
            err("matrix 结果测量越界 %s：%s" % (cells[0], cells[6]))
        if cells[7] not in DATA_KIND:
            err("matrix 数据类型越界 %s：%s" % (cells[0], cells[7]))

    idx = json.loads(read(os.path.join(VAULT, "index.json")))
    if len(idx.get("papers", [])) != 26:
        err("index.json 论文条数 %d" % len(idx.get("papers", [])))
    if len(idx.get("groups", [])) != 6:
        err("index.json 分组条数 %d" % len(idx.get("groups", [])))
    if sum(g["count"] for g in idx["groups"]) != 26:
        err("index.json 分组计数不合")
    for p in idx["papers"]:
        if p["data_kind"] not in DATA_KIND:
            err("index.json data_kind 越界 %s" % p["id"])
        if not os.path.isfile(os.path.join(VAULT, p["note"])):
            err("index.json note 路径不存在 %s" % p["id"])
        if p["links"] != sorted(name_to_id[t] for t in link_map[p["id"]]):
            err("index.json links 与卡片不一致 %s" % p["id"])
        if p["venue"] != papers[p["id"]]["venue"] or p["year"] != papers[p["id"]]["year"]:
            err("index.json 题录不符 %s" % p["id"])

    readme = read(os.path.join(VAULT, "README.md"))
    if len(readme.rstrip("\n").split("\n")) > 40:
        err("README 行数 %d 超过 40" % len(readme.rstrip("\n").split("\n")))

    for rel in expected:
        if not rel.endswith(".md"):
            continue
        full = os.path.join(VAULT, rel)
        if os.path.isfile(full):
            check_writing(rel, read(full))

    print("errors: %d" % len(errors))
    for e in errors:
        print("  - " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
