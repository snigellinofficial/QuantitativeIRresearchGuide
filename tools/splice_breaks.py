# -*- coding: utf-8 -*-
"""用改写后的拆解替换原内容。结束位置取下一个 h4 或 trace 容器的闭合标签。"""
import io
import os
import re

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()

blocks = {}
for fn in ("_d8b.html", "_d9b.html", "_d10b.html", "_d1112b.html", "_d1314b.html"):
    t = io.open(os.path.join(ROOT, "tools", fn), encoding="utf-8").read()
    for m in re.finditer(r'<h4 id="(d\d+-\d+)">.*?(?=<h4 id="d\d+-\d+">|\Z)', t, flags=re.S):
        blocks[m.group(1)] = m.group(0).rstrip() + "\n"

print("待替换", len(blocks))


def find_end(s, start):
    nxt = s.find('<h4 id="d', start + 1)
    # trace 容器结束：</div> 之后紧跟 </section>
    trace_end = -1
    for m in re.finditer(r"</div>\s*</section>", s[start:]):
        trace_end = start + m.start()
        break
    cands = [x for x in (nxt, trace_end) if x > 0]
    return min(cands)


for hid in sorted(blocks, key=lambda x: (int(x[1:].split("-")[0]), int(x.split("-")[1]))):
    start = s.find('<h4 id="%s">' % hid)
    if start < 0:
        print("缺失", hid)
        continue
    end = find_end(s, start)
    s = s[:start] + blocks[hid] + "\n" + s[end:]

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
