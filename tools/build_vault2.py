# -*- coding: utf-8 -*-
"""把 catalog-v2.json 与人工撰写的卡片正文合成为 vault-v2。"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vault2_links import adjacency, build_edges
from vault2_notes_fm import NOTES_FM
from vault2_notes_gc import NOTES_GC
from vault2_notes_nl import NOTES_NL
from vault2_notes_si import NOTES_SI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "catalog-v2.json")
VAULT = os.path.join(ROOT, "vault-v2")

NOTES = {}
NOTES.update(NOTES_GC)
NOTES.update(NOTES_SI)
NOTES.update(NOTES_NL)
NOTES.update(NOTES_FM)

SURNAME = {
    "G01": "henderson", "G02": "dell", "G03": "donaldson", "G04": "baum-snow",
    "G05": "faber", "G06": "banerjee", "G07": "michalopoulos", "G08": "michalopoulos",
    "G09": "dinkelman", "G10": "ahlfeldt", "G11": "asher", "G12": "burgess",
    "G13": "jedwab", "G14": "lipscomb", "G15": "müller-crepon", "G16": "hodler",
    "C01": "fearon", "C02": "gleditsch", "C03": "miguel", "C04": "raleigh",
    "C05": "sundberg", "C06": "hegre", "C07": "dube", "C08": "cederman",
    "C09": "berman", "C10": "tollefsen", "C11": "bazzi",
    "C12": "sanchez-de-la-sierra", "C13": "ash",
    "S01": "farrell", "S02": "fajgelbaum", "S03": "amiti", "S04": "ilzetzki",
    "S05": "gopinath", "S06": "morgan", "S07": "benguria", "S08": "crozet",
    "S09": "ahn", "S10": "kelley", "S11": "chen", "S12": "cha", "S13": "petry",
    "I01": "alesina", "I02": "abbott", "I03": "nielson", "I04": "dreher",
    "I05": "haftel", "I06": "blair", "I07": "abbott", "I08": "carnegie",
    "I09": "tallberg", "I10": "blair", "I11": "koremenos", "I12": "putnam",
    "N01": "carvalho", "N02": "banerjee", "N03": "boehm", "N04": "cranmer",
    "N05": "elliott", "N06": "dorussen", "N07": "maoz", "N08": "cederman",
    "N09": "cranmer", "N10": "kinne", "N11": "ward",
    "L01": "dell", "L02": "hsiang", "L03": "dell", "L04": "barreca",
    "L05": "deschenes", "L06": "carleton", "L07": "cattaneo", "L08": "marchiori",
    "L09": "bohra-mishra", "L10": "missirian", "L11": "couttenier",
    "F01": "chernozhukov", "F02": "grimmer", "F03": "wager", "F04": "mullainathan",
    "F05": "jean", "F06": "athey", "F07": "chen", "F08": "blumenstock",
    "F09": "wilkerson", "F10": "aiken", "F11": "ratledge", "F12": "fiaschi",
    "M01": "callaway", "M02": "goodman-bacon", "M03": "sun", "M04": "de-chaisemartin",
    "M05": "abadie", "M06": "abadie", "M07": "abadie", "M08": "borusyak",
    "M09": "adao", "M10": "cameron", "M11": "king", "M12": "collier",
}

TOPIC_FILE = {
    "G": "01-G-地理与基础设施.md",
    "C": "02-C-冲突与政治暴力.md",
    "S": "03-S-制裁与经济治国.md",
    "I": "04-I-国际制度与援助.md",
    "N": "05-N-网络与等级.md",
    "L": "06-L-气候迁移与灾害.md",
    "F": "07-F-测量与机器学习.md",
    "M": "08-M-方法论基石.md",
}

TOPIC_INTRO = {
    "G": "把地理距离写进处理变量，用路网、边界与地形提供外生变动。",
    "C": "把冲突发生写成资源、气候与制度条件的函数，单元多为国家—年或网格—月。",
    "S": "把价格变动与依赖结构当作权力的载体，单元多为企业、产品或国家对。",
    "I": "把制度条款与援助分配编码成可比较的变量，识别来源多为席位与时点。",
    "N": "把行为体的联系写成矩阵，用中心性、整图似然或网络形成刻画结构。",
    "L": "把气象冲击当作外生变动，结果覆盖增长、死亡率、迁移与冲突。",
    "F": "把不可直接观测的量用影像、文本与手机信号代理，误差本身是研究对象。",
    "M": "给出估计与推断的一般工具，讨论对象是估计量而非具体案例。",
}

LEVEL_NOTE = {
    1: "以描述统计与多元回归为主，识别依赖条件独立假设。",
    2: "以面板固定效应与双重差分为主，识别依赖组别与年份的对照。",
    3: "以工具变量、断点、合成控制与份额移动为主，识别依赖外生变动。",
    4: "以网络模型、结构模型与机器学习测量为主，识别依赖模型设定与验证。",
    5: "以方法学前沿为主，关注异质处理效应、空间推断与聚合偏差。",
}


def note_name(pid):
    return "%s-%s" % (pid, SURNAME[pid])


def note_path(pid):
    return "notes/%s.md" % note_name(pid)


def write(path, text):
    full = os.path.join(VAULT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def yaml_str(value):
    return json.dumps(value, ensure_ascii=False)


def render_note(pid, cat_paper, body, adj):
    lines = ["---"]
    lines.append("id: %s" % pid)
    lines.append("topic: %s" % cat_paper["topic"])
    lines.append("short: %s" % yaml_str(cat_paper["short"]))
    lines.append("authors: %s" % yaml_str(cat_paper["authors"]))
    lines.append("year: %d" % cat_paper["year"])
    lines.append("title: %s" % yaml_str(cat_paper["title"]))
    lines.append("venue: %s" % yaml_str(cat_paper["venue"]))
    lines.append("volume: %s" % yaml_str(cat_paper["volume"]))
    lines.append("doi: %s" % yaml_str(cat_paper["doi"]))
    lines.append("cites: %d" % cat_paper["cites"])
    lines.append("difficulty: %d" % cat_paper["difficulty"])
    lines.append("data_kind: %s" % yaml_str(cat_paper["data_kind"]))
    lines.append("design: %s" % yaml_str(cat_paper["design"]))
    lines.append("unit: %s" % yaml_str(cat_paper["unit"]))
    lines.append("tags: [%s]" % ", ".join(body["tags"]))
    lines.append("---")
    lines.append("")
    lines.append("# %s %s" % (pid, cat_paper["short"]))
    lines.append("")
    lines.append("## 一句话概括")
    lines.append("")
    lines.append(body["summary"])
    lines.append("")
    lines.append("## 研究设计")
    lines.append("")
    lines.append("- **观测单元** %s。" % cat_paper["unit"])
    lines.append("- **处理变量** %s" % body["treatment"])
    lines.append("- **结果变量** %s" % body["outcome"])
    lines.append("- **识别逻辑** %s" % body["identify"])
    lines.append("")
    lines.append("## 数据结构")
    lines.append("")
    for item in body["data"]:
        lines.append("- %s" % item)
    lines.append("")
    lines.append("## 可迁移的做法")
    lines.append("")
    for idx, item in enumerate(body["steps"], 1):
        lines.append("%d. %s" % (idx, item))
    lines.append("")
    lines.append("## 主要结论")
    lines.append("")
    for item in body["finding"]:
        lines.append("- %s" % item)
    lines.append("")
    lines.append("## 复制这项研究需要注意")
    lines.append("")
    for item in body["pitfall"]:
        lines.append("- %s" % item)
    lines.append("")
    lines.append("## 关联文献")
    lines.append("")
    for target in sorted(adj[pid]):
        _cat, reason = adj[pid][target]
        lines.append("- [[%s]] %s" % (note_name(target), reason))
    lines.append("")
    return "\n".join(lines)


def level_counts(ids, cat):
    counts = {lvl: 0 for lvl in range(1, 6)}
    for pid in ids:
        counts[cat[pid]["difficulty"]] += 1
    return counts


def render_topic_file(tid, name, members, cat, adj, all_ids):
    counts = level_counts(members, cat)
    dist = "、".join("%d 级 %d 篇" % (lvl, counts[lvl]) for lvl in range(1, 6) if counts[lvl])
    out = []
    out.append("# %s %s" % (tid, name))
    out.append("")
    out.append("| 项目 | 内容 |")
    out.append("| --- | --- |")
    out.append("| 专题编号 | %s |" % tid)
    out.append("| 篇数 | %d |" % len(members))
    out.append("| 难度分布 | %s |" % dist)
    out.append("| 共同思路 | %s |" % TOPIC_INTRO[tid])
    out.append("")
    out.append("## 成员一览")
    out.append("")
    out.append("| 编号 | 简称 | 年份 | 期刊 | 难度 | 数据形态 | 识别策略 | 卡片 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for pid in members:
        c = cat[pid]
        out.append("| %s | %s | %d | %s | %d | %s | %s | [[%s]] |" % (
            pid, c["short"], c["year"], c["venue"], c["difficulty"],
            c["data_kind"], c["design"], note_name(pid)))
    out.append("")
    out.append("## 组内关联")
    out.append("")
    out.append("| 起点 | 终点 | 归类 |")
    out.append("| --- | --- | --- |")
    inner = []
    cross = []
    for pid in members:
        for other in sorted(adj[pid]):
            cat_label = adj[pid][other][0]
            if cat[other]["topic"] == tid:
                if pid < other:
                    inner.append((pid, other, cat_label))
            else:
                cross.append((pid, other, cat_label))
    for a, b, label in inner:
        out.append("| [[%s]] | [[%s]] | %s |" % (note_name(a), note_name(b), label))
    out.append("")
    out.append("## 跨组关联")
    out.append("")
    out.append("| 本组卡片 | 对方卡片 | 对方专题 | 归类 |")
    out.append("| --- | --- | --- | --- |")
    for a, b, label in cross:
        out.append("| [[%s]] | [[%s]] | %s | %s |" % (
            note_name(a), note_name(b), cat[b]["topic"], label))
    out.append("")
    return "\n".join(out)


def render_matrix(cat, order, legend):
    out = []
    out.append("# 对照矩阵")
    out.append("")
    out.append("## 难度五级")
    out.append("")
    out.append("| 级别 | 定义 |")
    out.append("| --- | --- |")
    for lvl in range(1, 6):
        out.append("| %d | %s |" % (lvl, legend[str(lvl)]))
    out.append("")
    out.append("## 矩阵")
    out.append("")
    out.append("| 编号 | 简称 | 专题 | 难度 | 观测单元 | 识别策略 | 数据形态 | 期刊 | 年份 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for pid in order:
        c = cat[pid]
        out.append("| %s | %s | %s | %d | %s | %s | %s | %s | %d |" % (
            pid, c["short"], c["topic"], c["difficulty"], c["unit"],
            c["design"], c["data_kind"], c["venue"], c["year"]))
    out.append("")
    return "\n".join(out)


def render_ladder(cat, order, topics):
    out = []
    out.append("# 方法难度阶梯")
    out.append("")
    out.append("难度取值一至五，定义与对照矩阵同源。")
    out.append("")
    for lvl in range(1, 6):
        ids = [pid for pid in order if cat[pid]["difficulty"] == lvl]
        out.append("## %d 级" % lvl)
        out.append("")
        out.append(LEVEL_NOTE[lvl])
        out.append("")
        for pid in ids:
            body = NOTES[pid]
            out.append("- %s %s：%s" % (pid, cat[pid]["short"], body["contrib"]))
        out.append("")
    out.append("## 难度与专题交叉计数")
    out.append("")
    out.append("| 专题 | 1 级 | 2 级 | 3 级 | 4 级 | 5 级 | 合计 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    totals = {lvl: 0 for lvl in range(1, 6)}
    for t in topics:
        tid = t["id"]
        row = {lvl: 0 for lvl in range(1, 6)}
        for pid in order:
            if cat[pid]["topic"] == tid:
                row[cat[pid]["difficulty"]] += 1
                totals[cat[pid]["difficulty"]] += 1
        out.append("| %s %s | %s | %d |" % (
            tid, t["name"], " | ".join(str(row[lvl]) for lvl in range(1, 6)),
            sum(row.values())))
    out.append("| 合计 | %s | %d |" % (
        " | ".join(str(totals[lvl]) for lvl in range(1, 6)), sum(totals.values())))
    out.append("")
    return "\n".join(out)


def render_index_md(cat, topics, order, legend):
    out = []
    out.append("# 地理量化文献综述文献库")
    out.append("")
    out.append("| 项目 | 取值 |")
    out.append("| --- | --- |")
    out.append("| 文献数 | %d |" % len(order))
    out.append("| 专题数 | %d |" % len(topics))
    out.append("| 卡片目录 | notes/ |")
    out.append("| 生成日期 | 2026-10-29 |")
    out.append("| 引用量口径 | Crossref is-referenced-by-count |")
    out.append("")
    out.append("## 专题索引")
    out.append("")
    out.append("| 专题 | 名称 | 篇数 | 文件 |")
    out.append("| --- | --- | --- | --- |")
    for t in topics:
        n = len([pid for pid in order if cat[pid]["topic"] == t["id"]])
        out.append("| %s | %s | %d | [[%s]] |" % (
            t["id"], t["name"], n, TOPIC_FILE[t["id"]].replace(".md", "")))
    out.append("")
    out.append("## 八个分组表")
    out.append("")
    for t in topics:
        out.append("### %s %s" % (t["id"], t["name"]))
        out.append("")
        out.append("| 编号 | 简称 | 年份 | 难度 | 数据形态 | 识别策略 | 卡片 |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for pid in order:
            if cat[pid]["topic"] != t["id"]:
                continue
            c = cat[pid]
            out.append("| %s | %s | %d | %d | %s | %s | [[%s]] |" % (
                pid, c["short"], c["year"], c["difficulty"], c["data_kind"],
                c["design"], note_name(pid)))
        out.append("")
    out.append("## 难度分布")
    out.append("")
    out.append("| 难度 | 定义 | 篇数 |")
    out.append("| --- | --- | --- |")
    for lvl in range(1, 6):
        n = len([pid for pid in order if cat[pid]["difficulty"] == lvl])
        out.append("| %d | %s | %d |" % (lvl, legend[str(lvl)], n))
    out.append("")
    out.append("## 交叉引用")
    out.append("")
    out.append("| 项目 | 取值 |")
    out.append("| --- | --- |")
    out.append("| 关联对数 | %d |" % EDGE_TOTAL)
    out.append("| 数据形态相同 | %d |" % EDGE_CAT["数据形态相同"])
    out.append("| 识别逻辑相同 | %d |" % EDGE_CAT["识别逻辑相同"])
    out.append("| 互为稳健性检验 | %d |" % EDGE_CAT["互为稳健性检验"])
    out.append("| 每卡关联数 | 三至五条 |")
    out.append("")
    out.append("三类关联分别对应数据形态、识别逻辑与稳健性检验。")
    out.append("每条关联双向成立，两端卡片的关联文献一节都写出对方。")
    out.append("跨专题与专题内的关联都计入上表的条数。")
    out.append("")
    return "\n".join(out)


def render_readme():
    return "\n".join([
        "# 地理量化文献综述文献库",
        "",
        "## 目录",
        "",
        "| 路径 | 内容 |",
        "| --- | --- |",
        "| `00-index.md` | 分组表、难度分布、交叉引用统计 |",
        "| `01-G` 至 `08-M` | 八个专题的成员表与关联表 |",
        "| `notes/` | 一百张文献卡片 |",
        "| `matrix.md` | 一百行九列对照矩阵 |",
        "| `ladder.md` | 五级难度阶梯与交叉计数 |",
        "| `index.json` | 机器可读索引 |",
        "",
        "## 命名",
        "",
        "卡片文件名为编号加第一作者姓氏小写。",
        "",
        "## 卡片七节",
        "",
        "| 序号 | 节标题 |",
        "| --- | --- |",
        "| 1 | 一句话概括 |",
        "| 2 | 研究设计 |",
        "| 3 | 数据结构 |",
        "| 4 | 可迁移的做法 |",
        "| 5 | 主要结论 |",
        "| 6 | 复制这项研究需要注意 |",
        "| 7 | 关联文献 |",
        "",
        "## 关联",
        "",
        "| 项目 | 取值 |",
        "| --- | --- |",
        "| 归类 | 数据形态相同、识别逻辑相同、互为稳健性检验 |",
        "| 方向与条数 | 双向成立，两端都写出对方，每卡三至五条 |",
        "",
        "## 出处",
        "",
        "题录取自 `catalog-v2.json`，核验日期为 2026-10-29。",
        "引用量为 Crossref 口径。",
        "",
    ])


EDGE_TOTAL = 0
EDGE_CAT = {}


def main():
    global EDGE_TOTAL, EDGE_CAT
    with open(CATALOG, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    meta = data["meta"]
    legend = meta["difficulty_legend"]
    topics = data["topics"]
    cat = {p["id"]: p for p in data["papers"]}
    order = [p["id"] for p in data["papers"]]

    assert set(order) == set(NOTES), "卡片正文与题录编号不一致"
    assert set(order) == set(SURNAME), "姓氏表与题录编号不一致"
    assert len(order) == meta["n_papers"]

    edges = build_edges(cat, order)
    EDGE_TOTAL = len(edges)
    EDGE_CAT = {"数据形态相同": 0, "识别逻辑相同": 0, "互为稳健性检验": 0}
    for e in edges:
        EDGE_CAT[e["cat"]] += 1
    adj = adjacency(edges)

    for pid in order:
        write(note_path(pid), render_note(pid, cat[pid], NOTES[pid], adj))
    for t in topics:
        members = [pid for pid in order if cat[pid]["topic"] == t["id"]]
        write(TOPIC_FILE[t["id"]],
              render_topic_file(t["id"], t["name"], members, cat, adj, order))
    write("matrix.md", render_matrix(cat, order, legend))
    write("ladder.md", render_ladder(cat, order, topics))
    write("00-index.md", render_index_md(cat, topics, order, legend))
    write("README.md", render_readme())

    topics_json = []
    for t in topics:
        topics_json.append({
            "id": t["id"],
            "name": t["name"],
            "count": len([pid for pid in order if cat[pid]["topic"] == t["id"]]),
            "file": TOPIC_FILE[t["id"]],
        })
    papers_json = []
    for pid in order:
        c = cat[pid]
        papers_json.append({
            "id": pid,
            "short": c["short"],
            "topic": c["topic"],
            "difficulty": c["difficulty"],
            "year": c["year"],
            "venue": c["venue"],
            "note": note_path(pid),
            "links": sorted(adj[pid]),
        })
    payload = {
        "generated": "2026-10-29",
        "difficulty_legend": {str(k): v for k, v in legend.items()},
        "topics": topics_json,
        "papers": papers_json,
    }
    write("index.json", json.dumps(payload, ensure_ascii=False, indent=1) + "\n")

    print("notes: %d" % len(order))
    print("topics: %d" % len(topics))
    print("edges: %d" % len(edges))
    print("edge cat: %s" % EDGE_CAT)


if __name__ == "__main__":
    main()
