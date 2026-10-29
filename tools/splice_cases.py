# -*- coding: utf-8 -*-
"""把七篇文献拆解插入对应专题，替换重复的案例，更新目录。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 1 插入拆解
for i in range(8, 15):
    frag = io.open(os.path.join(ROOT, "tools", "_d%d.html" % i), encoding="utf-8").read()
    # 给小节标题一个锚点
    frag = frag.replace("<h3>%d.4　第二部分　文献拆解</h3>" % i,
                        '<h3 id="d%d">%d.4　第二部分　文献拆解</h3>' % (i, i))
    # 在专题章节的结尾插入
    start = s.find('<section id="c%d">' % i)
    assert start > 0, i
    end = s.find("</section>", start)
    assert end > start
    s = s[:end] + frag + "\n" + s[end:]
    print("inserted ch", i, len(frag))

# ---------------------------------------------------------------- 2 替换案例四
old_head = "案例四　矿产价格与冲突：价格冲击乘本地禀赋"
new_head = "案例四　区域偏袒与夜光：三层固定效应"
assert old_head in s
s = s.replace(old_head, new_head, 1)

old_meta_start = s.find('<p class="case-meta">Berman、Couttenier、Rohner 与 Thoenig（2017）')
assert old_meta_start > 0
old_meta_end = s.find("</p>", old_meta_start) + 4
s = s[:old_meta_start] + (
    '<p class="case-meta">Hodler 与 Raschky（2014），Quarterly Journal of Economics 129(4)，'
    'Crossref 引用 746，难度 3</p>') + s[old_meta_end:]

# 案例四正文整体替换
a = s.find('<h4>第一步　问题</h4>', s.find("案例四　区域偏袒与夜光"))
b = s.find("</div>", a)
assert a > 0 and b > a

NEW = """<h4>第一步　问题</h4>
<p>国家领导人的族群聚居区，是否在其执政期间获得更多公共资源？</p>

<h4>第二步　数据</h4>
<table class="gen">
<thead><tr><th>数据</th><th>形态</th><th>用途</th></tr></thead>
<tbody>
<tr><td>全球夜光栅格（一平方公里）</td><td>栅格</td><td>结果变量</td></tr>
<tr><td>族群分布多边形</td><td>面</td><td>处理的空间维度</td></tr>
<tr><td>领导人出生地、族群归属与任期</td><td>属性表</td><td>处理的时间维度</td></tr>
</tbody>
</table>

<h4>第三步　变量的构造</h4>
<p>对每个夜光像素，判断它落在哪个族群家园内。再判断该族群是否为当期领导人的族群。两个判断相乘，得到「同族群且在位」的指示。<strong>这一步把两个维度压成一个二值变量，故处理的变动只能来自领导人更替。</strong></p>

<h4>第四步　识别假设</h4>
<p>在控制了像素、国家—年、族群—年三层固定效应之后，领导人更替的时点与像素层面的其他冲击无关。<strong>这一假设可以部分检验：若更替前三年已出现亮度上升，假设就不成立。</strong></p>

<h4>第五步　方程</h4>
<div class="eq">
$$L_{pct}=\\beta\\,D_{pct}+\\mu_{p}+\\lambda_{ct}+\\delta_{et}+\\varepsilon_{pct}$$
</div>
<table class="sym">
<caption>案例四的估计方程与符号分配</caption>
<thead><tr><th>符号</th><th>含义</th><th>吸收了什么</th></tr></thead>
<tbody>
<tr><td>$L_{pct}$</td><td>像素 $p$ 在国家 $c$ 第 $t$ 年的夜光</td><td>结果变量</td></tr>
<tr><td>$D_{pct}$</td><td>像素所属族群是否为当权者族群</td><td>核心处理</td></tr>
<tr><td>$\\mu_p$</td><td>像素固定效应</td><td>地形、区位、历史</td></tr>
<tr><td>$\\lambda_{ct}$</td><td>国家—年固定效应</td><td>该国当年的宏观冲击</td></tr>
<tr><td>$\\delta_{et}$</td><td>族群—年固定效应</td><td>该族群当年的共同冲击</td></tr>
<tr><td>$\\beta$</td><td>偏袒的净效应</td><td>核心待估参数</td></tr>
</tbody>
</table>

<h4>第六步　稳健性</h4>
<p>四项。只保留族群边界附近的像素。按制度质量分组。把夜光换成人口密度。排除首都所在区域。<strong>第一项与第四项最关键：前者排除族群间的地理差异，后者排除首都的政治集聚。</strong></p>

<h4>第七步　复制要点</h4>
<p>三层固定效应最容易写错。判断标准是：<strong>处理变量的变动必须来自某个固定效应没有吸收的维度。</strong>若 $D$ 只随族群与年变化，则 $\\delta_{et}$ 会把它全部吸收，模型无法识别。</p>
"""

s = s[:a] + NEW + s[b:]

# ---------------------------------------------------------------- 3 更新案例表与目录
s = s.replace("<tr><td>4</td><td>矿产价格与冲突</td><td>价格冲击乘本地禀赋</td><td>3</td><td>C09</td></tr>",
              "<tr><td>4</td><td>区域偏袒与夜光</td><td>三层固定效应</td><td>3</td><td>G16</td></tr>")

toc_old = """    <li><a href="#c8">8　专题一　地理、可达性与基础设施</a></li>
    <li><a href="#c9">9　专题二　冲突、资源与政治暴力</a></li>
    <li><a href="#c10">10　专题三　制裁、经济治国与全球价值链</a></li>
    <li><a href="#c11">11　专题四　国际制度、援助与发展</a></li>
    <li><a href="#c12">12　专题五　网络、依赖与等级</a></li>
    <li><a href="#c13">13　专题六　气候、迁移与灾害</a></li>
    <li><a href="#c14">14　专题七　测量、机器学习与前沿</a></li>"""
toc_new = """    <li><a href="#c8">8　专题一　地理、可达性与基础设施</a>
      <ol class="sub"><li><a href="#d8">8.4　文献拆解</a></li></ol>
    </li>
    <li><a href="#c9">9　专题二　冲突、资源与政治暴力</a>
      <ol class="sub"><li><a href="#d9">9.4　文献拆解</a></li></ol>
    </li>
    <li><a href="#c10">10　专题三　制裁、经济治国与全球价值链</a>
      <ol class="sub"><li><a href="#d10">10.4　文献拆解</a></li></ol>
    </li>
    <li><a href="#c11">11　专题四　国际制度、援助与发展</a>
      <ol class="sub"><li><a href="#d11">11.4　文献拆解</a></li></ol>
    </li>
    <li><a href="#c12">12　专题五　网络、依赖与等级</a>
      <ol class="sub"><li><a href="#d12">12.4　文献拆解</a></li></ol>
    </li>
    <li><a href="#c13">13　专题六　气候、迁移与灾害</a>
      <ol class="sub"><li><a href="#d13">13.4　文献拆解</a></li></ol>
    </li>
    <li><a href="#c14">14　专题七　测量、机器学习与前沿</a>
      <ol class="sub"><li><a href="#d14">14.4　文献拆解</a></li></ol>
    </li>"""
assert toc_old in s
s = s.replace(toc_old, toc_new, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
print("sections", re.findall(r'<section id="([^"]+)"', s))
print("拆解锚点", re.findall(r'id="(d\d+)"', s))
