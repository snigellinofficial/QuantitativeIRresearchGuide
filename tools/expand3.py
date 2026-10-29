# -*- coding: utf-8 -*-
"""补足剩余五篇，包裹拆解区块，重建三级目录。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 1 补齐字数
ADDS = [
("另一个遗留问题是企业退出与贸易转移：出口下降可能只是换了承运方。</p>",
 "<strong>这两条都指向同一个技术条件：需要企业层面的中间投入数据，才能判断下降发生在哪一段。</strong>"),
("另一个遗留问题是关税的收入效应在财政年度之间如何分配。</p>",
 "<strong>若把关税收入计入福利而不扣除其扭曲成本，净损失会被系统性低估。</strong>"),
("另一个遗留问题是援助的部门构成未进入方程，而部门差异可能改变动机的估计。</p>",
 "<strong>把援助拆成基础设施、教育与治理三类重估，是后续文献常用的一步。</strong>"),
("另一个遗留问题是维数的选择缺少统计检验，只报告了不同维数下的稳定性。</p>",
 "<strong>缺少检验意味着维数仍是一个研究者的判断，而非数据的结论。</strong>"),
("另一个遗留问题是适应行为的内生：收入提高既带来适应，也部分来自气候本身。</p>",
 "<strong>两者在横截面上无法分开，只能靠长期面板与国别案例互补。</strong>"),
]
miss = []
for anchor, add in ADDS:
    k = s.find(anchor)
    if k < 0:
        miss.append(anchor[:24]); continue
    k += len(anchor) - 4  # 保留 </p>
    s = s[:k] + add + s[k:]
print("补齐未命中", len(miss), miss)

# ---------------------------------------------------------------- 2 包裹拆解区块
def wrap_traces(text):
    out = []
    pos = 0
    for m in re.finditer(r'<h4 id="d(\d+)-\d+">', text):
        start = m.start()
        # 找下一个 h4 或 </section>
        nxt_h4 = text.find('<h4 id="d', m.end())
        nxt_sec = text.find("</section>", m.end())
        cands = [x for x in (nxt_h4, nxt_sec) if x > 0]
        end = min(cands)
        out.append((start, end))
    # 从后往前插入，避免位移
    for start, end in reversed(out):
        text = text[:end] + "</div>" + text[end:]
        text = text[:start] + '<div class="trace">' + text[start:]
    return text

s = wrap_traces(s)
print("trace 区块", s.count('<div class="trace">'))

# ---------------------------------------------------------------- 3 给 h3 补 id
def add_ids(text):
    counter = {}
    def repl(m):
        num = m.group(2)
        ch = num.split(".")[0]
        counter[ch] = counter.get(ch, 0) + 1
        return '<h3 id="h%s-%d">%s%s</h3>' % (ch, counter[ch], m.group(1), m.group(3))
    return re.sub(r'(<h3)(>)(\d+\.\d+　[^<]*)</h3>', lambda m: repl(m), text), counter

# 只处理还没有 id 的 h3
def repl_h3(m):
    inner = m.group(1)
    return '<h3>%s</h3>' % inner

pat = re.compile(r'<h3>(\d+\.\d+　[^<]*)</h3>')
seen = {}
def r2(m):
    num = m.group(1).split("　")[0]
    ch = num.split(".")[0]
    seen[ch] = seen.get(ch, 0) + 1
    return '<h3 id="h%s-%d">%s</h3>' % (ch, seen[ch], m.group(1))
s = pat.sub(r2, s)
print("新增 h3 锚点", seen)

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
