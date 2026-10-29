# -*- coding: utf-8 -*-
"""两轮机检：语言风格与事实核验。

用法：
    python tools/check_academic.py --round style
    python tools/check_academic.py --round facts
    python tools/check_academic.py --round all --json report.json

退出码 0 表示通过。硬规则任一触发即退出码 1。
"""
import argparse
import csv
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
CAT = os.path.join(ROOT, "catalog-v2.json")
CSV = os.path.join(ROOT, "references.csv")

# 教材文体档案。学术期刊综述的目标见 style_vector 的 journal 档，此处按文体调整。
PROFILES = {
    "journal": {"L_mean": (42, 56), "L_long": (0.30, 0.50), "L_short": (0.15, 0.35), "L_max": 120},
    "textbook": {"L_mean": (30, 60), "L_long": (0.10, 0.50), "L_short": (0.10, 0.40), "L_max": 120},
}

BANNED = ["非常", "十分重要", "具有重要意义", "填补空白", "众所周知", "不言而喻",
          "毋庸置疑", "显而易见", "值得一提的是", "总而言之", "一言以蔽之",
          "丰富多彩", "日新月异", "极大", "极其重要", "十分关键", "至关重要",
          "我们认为", "笔者认为", "我们发现", "我们可以看到", "让我们", "笔者",
          "咱们", "其实", "反正", "搞", "弄", "一下", "挺"]


COLLOQ = ["都成立", "挺好", "好多", "差不多", "看看", "想想", "拿来", "搞",
          "弄", "一下子", "其实", "反正", "大概", "咱们", "人家", "啥",
          "怎么着", "这边", "那边", "说白了", "好比", "打个比方", "一上来"]

DEFENSIVE = ["仅供参考", "免责", "未逐段", "未获全文", "不可混用", "请注意",
             "需要说明", "需要指出", "本文档", "本交付", "谨慎使用", "以偏概全",
             "在所难免", "不足之处", "限于篇幅"]

LOW_VERBS = ["说过", "提到过", "研究过", "讨论过", "分析过", "指出过", "写过"]

CONNECTIVES = ["就", "而言", "据此", "其中", "然而", "因此", "相比之下",
               "更准确地说", "所以", "故", "从而", "进而", "同时", "此外", "但是"]

JUDGE = ["表明", "意味着", "构成", "取决于", "说明", "显示", "指向", "决定"]


CALLOUT = (r'<div class="(key|warn|def|note)"[^>]*>.*?</div>' + "|" +
           r'<div class="case"[^>]*>.*?</section>' + "|" +
           r'<ol class="enum">.*?</ol>')



SEMI_SUB = ("这", "该", "其", "此", "因此", "所以", "因为", "由于", "虽然",
            "如果", "当", "在")


def semicolon_bad(para):
    """分号只用于并列分句、多层复句的第一层与分项列举。

    只有后一分句以指代或从属连词起头、明显依附于前一分句时，才判为误用。
    """
    segs = [x for x in para.split("；") if x.strip()]
    if len(segs) < 2:
        return []
    bad = []
    for i in range(len(segs) - 1):
        r = segs[i + 1].strip()
        if r.startswith(SEMI_SUB) and len(re.findall(r"[\u4e00-\u9fff]", r)) >= 12:
            bad.append((segs[i][-12:], r[:12]))
    return bad


def visible_text(html, drop_callout=False):
    m = html[html.find("<main"):html.find("</main>")]
    if drop_callout:
        m = re.sub(CALLOUT, "\n", m, flags=re.S)
    m = re.sub(r"<script.*?</script>", " ", m, flags=re.S)
    m = re.sub(r"<style.*?</style>", " ", m, flags=re.S)
    m = re.sub(r"<h[1-4][^>]*>.*?</h[1-4]>", "\n", m, flags=re.S)
    m = re.sub(r"<table.*?</table>", "\n", m, flags=re.S)
    m = re.sub(r"<figure.*?</figure>", "\n", m, flags=re.S)
    m = re.sub(r"\$\$.*?\$\$", " MATH ", m, flags=re.S)
    m = re.sub(r"\$[^$]*\$", " MATH ", m)
    m = re.sub(r"<br\s*/?>", "\n", m)
    m = re.sub(r"</p>|</li>|</div>", "\n", m)
    m = re.sub(r"<[^>]+>", "", m)
    return m


def paragraphs(text):
    out = []
    for blk in text.split("\n"):
        blk = blk.strip()
        if len(re.findall(r"[\u4e00-\u9fff]", blk)) >= 20:
            out.append(blk)
    return out


def sentences(text):
    out = []
    for blk in paragraphs(text):
        for s in re.split(r"[。！？]", blk):
            s = s.strip()
            if re.findall(r"[\u4e00-\u9fff]", s):
                out.append(s)
    return out


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


# ---------------------------------------------------------------- 第一轮
def round_style(s, profile="textbook"):
    hard = []
    warn = []
    p = PROFILES[profile]

    chrome = re.sub(r"<header.*?</header>", " ", s, flags=re.S)
    chrome = re.sub(r"<nav.*?</nav>", " ", chrome, flags=re.S)
    plain = re.sub(r"<[^>]+>", "", chrome)
    plain = re.sub(r"\\$\\$.*?\\$\\$", " MATH ", plain, flags=re.S)
    plain = re.sub(r"\\$[^$]*\\$", " MATH ", plain)

    for w in COLLOQ:
        for m in re.finditer(re.escape(w), plain):
            hard.append(("H7 口语化表述", w, plain[max(0, m.start() - 16):m.start() + 16]))

    for w in DEFENSIVE:
        for m in re.finditer(re.escape(w), plain):
            hard.append(("H8 防御性文字", w, plain[max(0, m.start() - 16):m.start() + 16]))

    for w in BANNED:
        for m in re.finditer(re.escape(w), plain):
            hard.append(("H1 禁用词", w, plain[max(0, m.start() - 18):m.start() + 18]))

    for m in re.finditer("——", plain):
        hard.append(("H2 破折号插入", "——", plain[max(0, m.start() - 20):m.start() + 20]))

    COUNT = ("部分", "半", "类", "项", "件", "点", "步", "条", "层", "个",
             "方面", "章", "节", "如下", "以下", "形式", "包括", "原意", "原文",
             "概括", "表述", "写道", "分为", "共有", "问题", "理由是")
    for m in re.finditer("：([^。！？\\n]{15,})。", plain):
        pre = plain[max(0, m.start() - 14):m.start()]
        if any(w in pre for w in COUNT):
            continue  # 冒号引出对计数短语的展开，属规范用法
        hard.append(("H3 冒号引出完整句", m.group(0)[:30], ""))

    # 只把括号内含作者名的形式判为括号引用。作者在括号外的「作者（年份）」属参考文献制，不在此列。
    for m in re.finditer(r"（[^（）]{0,24}?[A-Za-zÀ-ÿ][^（）]{0,16}?(19|20)\d{2}[^（）]{0,8}?）", plain):
        hard.append(("H4 括号引用", m.group(0)[:26], ""))
    for m in re.finditer(r"（[^（）]{1,20}?, ?(19|20)\d{2}[^（）]{0,8}?）", plain):
        hard.append(("H4 括号引用", m.group(0)[:26], ""))


    for w in LOW_VERBS:
        for m in re.finditer(re.escape(w), s):
            hard.append(("H5 低级引述动词", w, s[max(0, m.start() - 16):m.start() + 16]))

    for m in re.finditer("[\U0001F300-\U0001FAFF\u2600-\u27BF]", plain):
        hard.append(("H6 emoji", m.group(0), ""))

    for para in paragraphs(visible_text(s)):
        for pair in semicolon_bad(para):
            hard.append(("H10 分号非并列", pair[0] + "｜" + pair[1], ""))
        segs = [x for x in para.split("；") if x.strip()]
        short = sum(1 for x in segs if len(re.findall(r"[\u4e00-\u9fff]", x)) < 20)
        if len(segs) >= 4 and short >= 2:
            warn.append(("W1 并列未分行", para[:34], "%d 段短句" % short))

    txt = visible_text(s, drop_callout=True)
    ss = sentences(txt)
    lens = [cn(x) for x in ss]
    n = len(lens) or 1
    L_mean = sum(lens) / n
    L_long = sum(1 for x in lens if x >= 60) / n
    L_short = sum(1 for x in lens if x <= 25) / n
    L_max = max(lens) if lens else 0

    body_cn = cn(txt) or 1
    semi = txt.count("；") / body_cn * 100
    conn = sum(txt.count(c) for c in CONNECTIVES) / body_cn * 100
    judge = sum(1 for x in ss if any(j in x for j in JUDGE)) / n

    paras = paragraphs(txt)
    p_sent = [len([y for y in re.split(r"[。！？]", x) if cn(y) > 0]) for x in paras]
    p_cn = [cn(x) for x in paras]

    vec = {
        "L_mean": round(L_mean, 1),
        "L_long": round(L_long, 3),
        "L_short": round(L_short, 3),
        "L_max": L_max,
        "分号密度": round(semi, 2),
        "连接词密度": round(conn, 2),
        "判断句比例": round(judge, 3),
        "段落句数均值": round(sum(p_sent) / len(p_sent), 2) if p_sent else 0,
        "段落字数均值": round(sum(p_cn) / len(p_cn), 1) if p_cn else 0,
        "句子总数": n,
        "正文字数": body_cn,
    }
    dev = []
    for k in ("L_mean", "L_long", "L_short"):
        lo, hi = p[k]
        if not (lo <= vec[k] <= hi):
            dev.append((k, vec[k], (lo, hi)))
    if vec["L_max"] > p["L_max"]:
        dev.append(("L_max", vec["L_max"], p["L_max"]))
    if not (0.3 <= vec["分号密度"] <= 2.0):
        dev.append(("分号密度", vec["分号密度"], (0.3, 2.0)))
    return hard, vec, dev, warn


# ---------------------------------------------------------------- 第二轮
class Balancer(HTMLParser):
    VOID = {"br", "img", "meta", "link", "input", "hr", "source"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack, self.err = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.err.append((tag, list(self.stack[-3:])))
            if tag in self.stack:
                del self.stack[self.stack.index(tag):]
            return
        self.stack.pop()


def round_facts(s):
    hard = []
    cat = json.load(open(CAT, encoding="utf-8"))
    ids = {p["id"] for p in cat["papers"]}
    dois = {p["doi"].lower() for p in cat["papers"]}

    # F1 csv 与目录一致
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != len(cat["papers"]):
        hard.append(("F1 CSV 行数不符", len(rows), len(cat["papers"])))
    csv_dois = {r["DOI"].lower() for r in rows}
    if csv_dois != dois:
        hard.append(("F1 CSV 与目录的 DOI 集合不一致",
                     len(csv_dois - dois), len(dois - csv_dois)))

    # F2 DOI 格式与唯一性
    bad = [d for d in dois if not re.match(r"^10\.\d{4,9}/", d)]
    if bad:
        hard.append(("F2 DOI 格式", bad[:3], len(bad)))
    all_doi = re.findall(r"10\.\d{4,9}/[^\s\"<>|）]+", s)
    dup = len(all_doi) - len(set(x.lower() for x in all_doi))
    if dup < 0:
        hard.append(("F2 DOI 重复", dup, ""))

    # F3 题录字段非空
    for p in cat["papers"]:
        for k in ("year", "venue", "doi", "title"):
            if not p.get(k):
                hard.append(("F3 字段为空", p["id"], k))

    # F4 正文编号可追溯
    used = set(re.findall(r"\b([GCFSNLIM]0\d)\b", s)) | set(re.findall(r"\b([GCFSNLIM]1\d)\b", s))
    ghost = used - ids
    if ghost:
        hard.append(("F4 正文出现目录外编号", sorted(ghost), len(ghost)))

    # F5 参考文献表行数
    ref = s[s.find('<section id="c17">'):s.find("</section>", s.find('<section id="c17">'))]
    n_rows = len(re.findall(r"<tr><td>[GCFSNLIM]\d\d</td>", ref))
    if n_rows != len(cat["papers"]):
        hard.append(("F5 参考文献表行数", n_rows, len(cat["papers"])))

    # F6 结构与资源
    b = Balancer()
    b.feed(s)
    if b.stack or b.err:
        hard.append(("F6 标签不平衡", b.err[:3], b.stack[:3]))
    lost = [m.group(1) for m in re.finditer(r'(?:src|href)="((?:assets|vault-v2|vault)/[^"]+)"', s)
            if not os.path.exists(os.path.join(ROOT, m.group(1)))]
    if lost:
        hard.append(("F6 资源缺失", lost[:3], len(lost)))
    ids_attr = set(re.findall(r'id="([^"]+)"', s))
    links = set(re.findall(r'href="#([^"]+)"', s))
    dead = links - ids_attr
    if dead:
        hard.append(("F6 失效锚点", sorted(dead)[:3], len(dead)))

    # F7 公式
    if s.count("$$") % 2 or s.replace("$$", "").count("$") % 2:
        hard.append(("F7 公式定界不成对", s.count("$$"), ""))
    for m in re.finditer(r"\$\$(.+?)\$\$", s, re.S):
        if any(ord(c) > 127 for c in m.group(1)):
            hard.append(("F7 公式内中文", m.group(1)[:40], ""))
            break

    # F8 表格列数
    for tm in re.finditer(r"<table[^>]*>(.*?)</table>", s, re.S):
        head = re.search(r"<thead>.*?<tr>(.*?)</tr>", tm.group(1), re.S)
        if not head:
            continue
        ncol = len(re.findall(r"<th[^>]*>", head.group(1)))
        for row in re.findall(r"<tr>(.*?)</tr>", tm.group(1), re.S):
            if "<td" in row and len(re.findall(r"<td[^>]*>", row)) != ncol:
                hard.append(("F8 表格列数不一致", row[:40], ncol))
                break

    stats = {"目录文献数": len(cat["papers"]), "CSV 行数": len(rows),
             "参考文献表行数": n_rows, "正文引用编号数": len(used),
             "DOI 出现次数": len(all_doi)}
    return hard, stats


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", default="all", choices=["style", "facts", "all"])
    ap.add_argument("--profile", default="textbook", choices=list(PROFILES))
    ap.add_argument("--json")
    a = ap.parse_args()

    s = open(HTML, encoding="utf-8").read()
    report = {}

    if a.round in ("style", "all"):
        hard, vec, dev, warn = round_style(s, a.profile)
        report["style"] = {"hard": hard, "vector": vec, "deviation": dev, "warning": warn}
        print("== 第一轮 语言风格（%s 档）==" % a.profile)
        print("   硬规则触发", len(hard))
        for h in hard[:12]:
            print("     ", h[0], "｜", h[1])
        print("   向量", json.dumps(vec, ensure_ascii=False))
        print("   偏离", dev if dev else "无")
        print("   段落级警告", len(warn))

    if a.round in ("facts", "all"):
        hard, stats = round_facts(s)
        report["facts"] = {"hard": hard, "stats": stats}
        print("== 第二轮 事实核验 ==")
        print("   硬规则触发", len(hard))
        for h in hard[:12]:
            print("     ", h[0], "｜", h[1])
        print("   统计", json.dumps(stats, ensure_ascii=False))

    if a.json:
        json.dump(report, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    failed = any(v["hard"] for v in report.values())
    print("结果:", "不通过" if failed else "通过")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
