# -*- coding: utf-8 -*-
"""把 catalog.json 与人工撰写的卡片正文合成为 vault。"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vault_papers_abc import PAPERS_ABC
from vault_papers_def import PAPERS_DEF
from vault_links import EDGES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "catalog.json")
VAULT = os.path.join(ROOT, "vault")

PAPERS = {}
PAPERS.update(PAPERS_ABC)
PAPERS.update(PAPERS_DEF)

SURNAME = {
    "A1": "dell", "A2": "michalopoulos", "A3": "michalopoulos", "A4": "burgess", "A5": "ahlfeldt",
    "B1": "donaldson", "B2": "faber", "B3": "asher", "B4": "jedwab", "B5": "baum-snow",
    "C1": "dinkelman", "C2": "lipscomb", "C3": "ratledge",
    "D1": "miguel", "D2": "berman", "D3": "tollefsen", "D4": "hodler",
    "E1": "cederman", "E2": "ward", "E3": "cranmer", "E4": "banerjee",
    "F1": "henderson", "F2": "jean", "F3": "aiken", "F4": "randhawa", "F5": "fiaschi",
}

GROUP_FILE = {
    "A": "01-group-A-断点与边界.md",
    "B": "02-group-B-可达性与基础设施.md",
    "C": "03-group-C-电力与能源设施.md",
    "D": "04-group-D-冲突资源与网格.md",
    "E": "05-group-E-网络与关系.md",
    "F": "06-group-F-测量卫星与前沿.md",
}

LINK_STYLE = {"数据形态相同": "---", "识别逻辑相同": "-.->", "互为稳健性检验": "==>"}

GROUP_LOGIC = {
    "A": "把一条画在地图上的线当作外生分界。线两侧的地理条件连续，制度或干预在线上跳变。",
    "B": "把路网换成成本矩阵，用最短路或市场准入衡量区位的相对优劣。工程规划的时间差提供识别来源。",
    "C": "电网扩张的落点由地形、河流落差与行政批次决定。这些落点与当地经济潜力弱相关。",
    "D": "把世界切成等面积方格。外部价格冲击乘上本地资源禀赋，得到随格子与时期变动的影响强度。",
    "E": "把行为体与联系写成矩阵。中心性、指数随机图与潜在空间把关系结构参数化。",
    "F": "把不可直接观测的经济量用可观测信号代理。代理关系本身是检验对象，不是论证前提。",
}


def note_name(pid):
    return "%s-%s" % (pid, SURNAME[pid])


def note_path(pid):
    return "notes/%s.md" % note_name(pid)


def load_catalog():
    with open(CATALOG, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build_links():
    adj = {}
    for pid in PAPERS:
        adj[pid] = {}
    for a, b, cat, ra, rb in EDGES:
        assert cat in LINK_STYLE, cat
        assert b not in adj[a], "重复边 %s-%s" % (a, b)
        assert a not in adj[b], "重复边 %s-%s" % (a, b)
        adj[a][b] = (cat, ra)
        adj[b][a] = (cat, rb)
    for pid in PAPERS:
        n = len(adj[pid])
        cross = [t for t in adj[pid] if PAPERS[t]["group"] != PAPERS[pid]["group"]]
        same = [t for t in adj[pid] if PAPERS[t]["group"] == PAPERS[pid]["group"]]
        assert 3 <= n <= 5, "%s 关联数 %d 越界" % (pid, n)
        assert len(cross) <= 2, "%s 跨组 %d 超限" % (pid, len(cross))
        assert len(same) >= 1, "%s 缺组内互链" % pid
    return adj


def write(path, text):
    full = os.path.join(VAULT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def yaml_value(value):
    if isinstance(value, int):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def render_note(pid, paper, cat_paper, adj):
    lines = ["---"]
    lines.append("id: %s" % pid)
    lines.append("group: %s" % paper["group"])
    lines.append("short: %s" % yaml_value(cat_paper["short"]))
    lines.append("authors: %s" % yaml_value(cat_paper["authors"]))
    lines.append("year: %s" % cat_paper["year"])
    lines.append("title: %s" % yaml_value(cat_paper["title"]))
    lines.append("venue: %s" % yaml_value(cat_paper["venue"]))
    lines.append("volume: %s" % yaml_value(cat_paper["volume"]))
    lines.append("doi: %s" % yaml_value(cat_paper["doi"]))
    lines.append("cites: %s" % cat_paper["cites"])
    lines.append("unit: %s" % yaml_value(cat_paper["unit"]))
    lines.append("design: %s" % yaml_value(paper["design_short"]))
    lines.append("tags: [%s]" % ", ".join(paper["tags"]))
    lines.append("---")
    lines.append("")
    lines.append("## 一句话概括")
    lines.append("")
    lines.append(paper["summary"])
    lines.append("")
    lines.append("## 研究设计")
    lines.append("")
    for item in paper["design"]:
        lines.append("- %s" % item)
    lines.append("")
    lines.append("## 数据结构")
    lines.append("")
    for item in paper["data"]:
        lines.append("- %s" % item)
    lines.append("")
    lines.append("## 可迁移的做法")
    lines.append("")
    for idx, item in enumerate(paper["steps"], 1):
        lines.append("%d. %s" % (idx, item))
    lines.append("")
    lines.append("## 主要结论")
    lines.append("")
    lines.append("".join(paper["finding"]))
    lines.append("")
    lines.append("## 复制这项研究需要注意")
    lines.append("")
    for item in paper["pitfall"]:
        lines.append("- %s" % item)
    lines.append("")
    lines.append("## 关联文献")
    lines.append("")
    for target in sorted(adj[pid]):
        _cat, reason = adj[pid][target]
        lines.append("- [[%s]] %s" % (note_name(target), reason))
    lines.append("")
    return "\n".join(lines)


def render_group(gid, group, papers_in_group, adj, cat):
    out = []
    out.append("# 组 %s %s" % (gid, group["name"]))
    out.append("")
    out.append("| 项目 | 内容 |")
    out.append("| --- | --- |")
    out.append("| 组编号 | %s |" % gid)
    out.append("| 中文名 | %s |" % group["name"])
    out.append("| 英文名 | %s |" % group["en"])
    out.append("| 篇数 | %d |" % len(papers_in_group))
    out.append("")
    out.append("## 分组逻辑")
    out.append("")
    out.append(GROUP_LOGIC[gid])
    out.append("")
    out.append("## 成员一览")
    out.append("")
    out.append("| 编号 | 简称 | 年份 | 期刊 | 观测单元 | 识别策略 | 卡片 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for pid in papers_in_group:
        c = cat[pid]
        out.append("| %s | %s | %d | %s | %s | %s | [[%s]] |" % (
            pid, c["short"], c["year"], c["venue"], c["unit"].split("，")[0],
            PAPERS[pid]["design_short"], note_name(pid)))
    out.append("")
    out.append("## 组内互链")
    out.append("")
    out.append("| 起点 | 终点 | 归类 |")
    out.append("| --- | --- | --- |")
    pairs = []
    for a, b, edge_cat, _ra, _rb in EDGES:
        if PAPERS[a]["group"] == gid and PAPERS[b]["group"] == gid:
            pairs.append((a, b, edge_cat))
    for a, b, edge_cat in pairs:
        out.append("| [[%s]] | [[%s]] | %s |" % (note_name(a), note_name(b), edge_cat))
    out.append("")
    out.append("## 跨组链接")
    out.append("")
    out.append("| 本组卡片 | 对方卡片 | 对方组 | 归类 |")
    out.append("| --- | --- | --- | --- |")
    cross_rows = []
    for a, b, edge_cat, _ra, _rb in EDGES:
        ga, gb = PAPERS[a]["group"], PAPERS[b]["group"]
        if ga == gid and gb != gid:
            cross_rows.append((a, b, gb, edge_cat))
        elif gb == gid and ga != gid:
            cross_rows.append((b, a, ga, edge_cat))
    for a, b, other, edge_cat in cross_rows:
        out.append("| [[%s]] | [[%s]] | %s | %s |" % (note_name(a), note_name(b), other, edge_cat))
    out.append("")
    return "\n".join(out)


def render_matrix(cat, order):
    out = []
    out.append("# 跨文献对照矩阵")
    out.append("")
    out.append("处理变量类型六种、结果变量测量方式五种，取值互斥且按论文归类。")
    out.append("")
    out.append("| 编号 | 简称 | 分组 | 观测单元 | 处理变量类型 | 识别策略 | 结果变量的测量方式 | 数据类型 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for pid in order:
        c = cat[pid]
        p = PAPERS[pid]
        unit = c["unit"].replace("|", "/")
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            pid, c["short"], p["group"], unit, p["treat_type"],
            p["design_short"], p["outcome_kind"], p["data_kind"]))
    out.append("")
    out.append("## 取值口径")
    out.append("")
    out.append("| 列 | 取值 | 口径 |")
    out.append("| --- | --- | --- |")
    treat_rows = [
        ("处理变量类型", "二值政策", "处理为是否受政策或制度覆盖的二元变量。"),
        ("处理变量类型", "连续暴露度", "处理为可连续变动的剂量，例如距离或指数。"),
        ("处理变量类型", "价格冲击交互", "外部价格变动乘本地禀赋，随单元与时期变动。"),
        ("处理变量类型", "网络位置", "行为体在关系结构中的位置，或整图的结构特征。"),
        ("处理变量类型", "代理测量", "处理或结果由模型预测值充当，误差结构是研究对象。"),
        ("处理变量类型", "无处理变量（数据基础设施）", "文献只提供数据单元与主键，不设处理。"),
        ("结果变量的测量方式", "行政统计", "来自普查、国民账户或行政报表。"),
        ("结果变量的测量方式", "遥感代理", "由遥感信号换算得到。"),
        ("结果变量的测量方式", "调查数据", "来自抽样入户调查。"),
        ("结果变量的测量方式", "冲突事件记录", "来自冲突事件数据库的计数或发生与否。"),
        ("结果变量的测量方式", "网络整体结构", "因变量为整张关系矩阵，而非单条边。"),
    ]
    for row in treat_rows:
        out.append("| %s | %s | %s |" % row)
    out.append("")
    return "\n".join(out)


def render_index_md(cat, groups, order, adj):
    out = []
    out.append("# 地理量化文献知识库")
    out.append("")
    out.append("## 分组")
    out.append("")
    out.append("| 组 | 名称 | 篇数 | 索引文件 | 共同识别逻辑 |")
    out.append("| --- | --- | --- | --- | --- |")
    for g in groups:
        n = len([p for p in order if PAPERS[p]["group"] == g["id"]])
        out.append("| %s | %s | %d | [[%s]] | %s |" % (
            g["id"], g["name"], n, GROUP_FILE[g["id"]].replace(".md", ""), GROUP_LOGIC[g["id"]]))
    out.append("")
    out.append("## 文献一览")
    out.append("")
    out.append("| 编号 | 简称 | 年份 | 期刊 | 观测单元 | 识别策略 | 数据形态 | 卡片 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for pid in order:
        c = cat[pid]
        out.append("| %s | %s | %d | %s | %s | %s | %s | [[%s]] |" % (
            pid, c["short"], c["year"], c["venue"], c["unit"].replace("，", "，"),
            PAPERS[pid]["design_short"], PAPERS[pid]["data_kind"], note_name(pid)))
    out.append("")
    out.append("## 交叉引用图")
    out.append("")
    out.append("实线为数据形态相同，点线为识别逻辑相同，粗箭头为互为稳健性检验。")
    out.append("")
    out.append("```mermaid")
    out.append("graph LR")
    for g in groups:
        out.append('  subgraph G%s["组 %s %s"]' % (g["id"], g["id"], g["name"]))
        for pid in order:
            if PAPERS[pid]["group"] == g["id"]:
                out.append('    %s["%s %s"]' % (pid, pid, cat[pid]["short"].replace('"', "")))
        out.append("  end")
    for a, b, edge_cat, _ra, _rb in EDGES:
        out.append("  %s %s %s" % (a, LINK_STYLE[edge_cat], b))
    out.append("```")
    out.append("")
    out.append("## 引用关系统计")
    out.append("")
    out.append("| 组 | 组内边 | 跨组边（按本组端点计） | 卡片数 |")
    out.append("| --- | --- | --- | --- |")
    for g in groups:
        inner = len([1 for a, b, _c, _ra, _rb in EDGES
                     if PAPERS[a]["group"] == g["id"] and PAPERS[b]["group"] == g["id"]])
        cross = len([1 for a, b, _c, _ra, _rb in EDGES
                     if g["id"] in (PAPERS[a]["group"], PAPERS[b]["group"])
                     and PAPERS[a]["group"] != PAPERS[b]["group"]])
        nodes = len([1 for p in order if PAPERS[p]["group"] == g["id"]])
        out.append("| %s | %d | %d | %d |" % (g["id"], inner, cross, nodes))
    out.append("")
    total_edge = len(EDGES)
    cross_total = len([1 for a, b, _c, _ra, _rb in EDGES
                       if PAPERS[a]["group"] != PAPERS[b]["group"]])
    out.append("全文共 %d 条关联边，其中跨组 %d 条，组内 %d 条。" % (
        total_edge, cross_total, total_edge - cross_total))
    out.append("")
    return "\n".join(out)


def render_readme(meta):
    return "\n".join([
        "# 地理量化文献知识库",
        "",
        "## 结构",
        "",
        "| 路径 | 内容 |",
        "| --- | --- |",
        "| `00-index.md` | 分组表、26 篇一览表、交叉引用图 |",
        "| `01` 至 `06-group-*.md` | 六组索引，含组内互链与跨组链接 |",
        "| `notes/` | 26 张文献卡片 |",
        "| `matrix.md` | 26 行 8 列对照矩阵，附取值口径 |",
        "| `index.json` | 机器可读索引，供 HTML 文档消费 |",
        "",
        "## 命名",
        "",
        "卡片文件名为「编号-第一作者姓氏小写」。",
        "",
        "## 卡片七节",
        "",
        "一句话概括、研究设计、数据结构、可迁移的做法、主要结论、复制这项研究需要注意、关联文献。",
        "",
        "## 链接",
        "",
        "关联只取三种归类，即数据形态相同、识别逻辑相同、互为稳健性检验。",
        "每条关联双向成立，两端的卡片都写出对方。",
        "每张卡片三至五条关联，跨组至多两条。",
        "",
        "## 出处",
        "",
        "题录与要点取自 `catalog.json`，核验日期为 %s。" % meta["retrieved"],
        "引用量为 OpenAlex 口径。",
        "",
    ])


def main():
    data = load_catalog()
    meta = data["meta"]
    groups = data["groups"]
    cat = {p["id"]: p for p in data["papers"]}
    order = [p["id"] for p in data["papers"]]

    assert set(order) == set(PAPERS), "卡片正文与题录编号不一致"
    assert len(order) == meta["n_papers"] == 26
    for pid in order:
        PAPERS[pid]["group"] = cat[pid]["group"]
    adj = build_links()

    for pid in order:
        write(note_path(pid), render_note(pid, PAPERS[pid], cat[pid], adj))
    for g in groups:
        members = [p for p in order if PAPERS[p]["group"] == g["id"]]
        write(GROUP_FILE[g["id"]], render_group(g["id"], g, members, adj, cat))
    write("matrix.md", render_matrix(cat, order))
    write("00-index.md", render_index_md(cat, groups, order, adj))
    write("README.md", render_readme(meta))

    groups_json = []
    for g in groups:
        groups_json.append({
            "id": g["id"],
            "name": g["name"],
            "count": len([p for p in order if PAPERS[p]["group"] == g["id"]]),
            "file": GROUP_FILE[g["id"]],
        })
    papers_json = []
    for pid in order:
        c = cat[pid]
        papers_json.append({
            "id": pid,
            "short": c["short"],
            "group": PAPERS[pid]["group"],
            "year": c["year"],
            "venue": c["venue"],
            "unit": c["unit"],
            "design": PAPERS[pid]["design_short"],
            "data_kind": PAPERS[pid]["data_kind"],
            "note": note_path(pid),
            "links": sorted(adj[pid]),
        })
    payload = {"generated": meta["retrieved"], "groups": groups_json, "papers": papers_json}
    write("index.json", json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    print("notes: %d" % len(order))
    print("groups: %d" % len(groups))
    print("edges: %d" % len(EDGES))


if __name__ == "__main__":
    main()
