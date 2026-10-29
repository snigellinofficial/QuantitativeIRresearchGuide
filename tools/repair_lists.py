# -*- coding: utf-8 -*-
"""修补列表项内被分号切断的强调标签，并把列表项排除出风格向量。"""
import io
import re

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
P = ROOT + r"\index.html"
s = io.open(P, encoding="utf-8").read()


def fix_li(m):
    body = m.group(1)
    o, c = body.count("<strong>"), body.count("</strong>")
    if o > c:
        body = body.rstrip() + "</strong>" * (o - c)
    elif c > o:
        body = "<strong>" * (c - o) + body
    return "<li>%s</li>" % body


s = re.sub(r"<li>((?:(?!</li>).)*?)</li>", fix_li, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s)

# 向量样本排除编号列表
p2 = ROOT + r"\tools\check_academic.py"
c = io.open(p2, encoding="utf-8").read()
old = 'CALLOUT = r\'<div class="(key|warn|def|note)"[^>]*>.*?</div>\' + "|" + r\'<div class="case"[^>]*>.*?</section>\''
new = ('CALLOUT = (r\'<div class="(key|warn|def|note)"[^>]*>.*?</div>\' + "|" +\n'
       '           r\'<div class="case"[^>]*>.*?</section>\' + "|" +\n'
       '           r\'<ol class="enum">.*?</ol>\')')
assert old in c
c = c.replace(old, new, 1)
io.open(p2, "w", encoding="utf-8").write(c)
print("列表项已排除出向量样本")
