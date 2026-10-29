# -*- coding: utf-8 -*-
"""修订序言与口语化表述，为并列结构建立可分行样式。"""
import io
import re

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
P = ROOT + r"\index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 1 序言重写
a = s.find('<p>三种读法都成立')
if a < 0:
    a = s.find('<p>三种读法')
b = s.find("</p>", a) + 4
NEW = """<p>以下三种读法均成立。</p>
<ol class="enum">
<li>按章序通读，适用于零基础的读者。</li>
<li>先读第 15 章的某一案例，再回到对应专题，适用于已有具体题目的读者。</li>
<li>只查方法与文献，适用于把本书当作工具书的读者。</li>
</ol>
<p>配套的 vault-v2 目录存放一百张文献卡片，每张含七节正文与双向链接。</p>"""
s = s[:a] + NEW + s[b:]

# 删去核验声明段（防御性文字不入正文）
k = s.find("<p>全部一百篇文献经 Crossref 逐条核验")
if k > 0:
    e = s.find("</p>", k) + 4
    s = s[:k] + s[e:]

# ---------------------------------------------------------------- 2 口语词
REPL = [
    ("都成立。", "均成立。"),
    ("挺", "较为"),
    ("特别", "尤其"),
    ("前面", "先前"),
    ("后面", "此后"),
    ("搞", "处理"),
    ("弄", "处理"),
    ("其实", "实际上"),
    ("反正", "无论如何"),
    ("大概", "约"),
    ("一下子", "一次"),
    ("看看", "检视"),
    ("想想", "考虑"),
    ("拿来", "取来"),
    ("差不多", "接近"),
]
for x, y in REPL:
    s = s.replace(x, y)

# ---------------------------------------------------------------- 3 计数式并列改为列表
STEP = re.compile(r"<p>([^<]{0,40}?(?:共有|分为|包括|依次为|有以下)?[^<]{0,12}?"
                  r"(?:三步|四步|五步|三点|四项|五项|三个|四个|五个|两类|三类)[^<]{0,12}?。)(.*?)</p>", re.S)


def to_list(m):
    head, body = m.group(1), m.group(2)
    if body.count("；") < 2 or "第一步" not in body and "第一，" not in body:
        return m.group(0)
    tail = ""
    mk = re.search(r"(第[一二三四五六]步[^；。]*。|第[一二三四五六]，[^；。]*。)$", body)
    parts = [x for x in re.split(r"；", body) if x.strip()]
    if len(parts) < 3:
        return m.group(0)
    items = []
    for x in parts:
        x = x.strip()
        x = re.sub(r"^(第[一二三四五六]步|第[一二三四五六])[，、]?", "", x)
        if not x.endswith("。"):
            x += "。"
        items.append("  <li>%s</li>" % x)
    return "<p>%s</p>\n<ol class=\"enum\">\n%s\n</ol>" % (head, "\n".join(items))


s2, n = STEP.subn(to_list, s)
print("并列段转列表", s2.count('<ol class="enum">') - s.count('<ol class="enum">'))
s = s2

# ---------------------------------------------------------------- 4 样式
css = io.open(ROOT + r"\assets\style.css", encoding="utf-8").read()
if ".enum{" not in css:
    css += """
/* 并列项分行：为三步、四项一类枚举提供独立行与序数 */
ol.enum{
  list-style:none;counter-reset:en;margin:14px 0 18px;padding:0 0 0 6px;
}
ol.enum>li{
  counter-increment:en;position:relative;
  padding:2px 0 8px 30px;
  font-size:16px;line-height:1.9;color:var(--ink);
}
ol.enum>li::before{
  content:counter(en);position:absolute;left:0;top:3px;
  width:20px;height:20px;line-height:20px;text-align:center;
  background:var(--blue-wash);color:var(--blue);
  border:1px solid #cfdaef;border-radius:3px;
  font-family:"Microsoft YaHei",sans-serif;font-size:12px;
}
.trace ol.enum>li{font-size:14.6px;line-height:1.95;padding-bottom:7px;}
"""
    io.open(ROOT + r"\assets\style.css", "w", encoding="utf-8").write(css)
    print("样式已追加")

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
