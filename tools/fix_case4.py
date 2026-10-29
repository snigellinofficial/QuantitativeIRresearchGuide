# -*- coding: utf-8 -*-
"""重写案例四，清掉替换时残留的重复段落与多余闭合标签。"""
import io

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

a = s.find('<div class="case" id="case4">')
b = s.find('<div class="case" id="case5">')
assert a > 0 and b > a, (a, b)

NEW = """<div class="case" id="case4">
<p class="case-head">案例四　区域偏袒与夜光：三层固定效应</p>
<p class="case-meta">Hodler 与 Raschky（2014），Quarterly Journal of Economics 129(4)，Crossref 引用 746，难度 3</p>

<h4>第一步　问题</h4>
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
<tr><td>$\\mu_{p}$</td><td>像素固定效应</td><td>地形、区位、历史</td></tr>
<tr><td>$\\lambda_{ct}$</td><td>国家—年固定效应</td><td>该国当年的宏观冲击</td></tr>
<tr><td>$\\delta_{et}$</td><td>族群—年固定效应</td><td>该族群当年的共同冲击</td></tr>
<tr><td>$\\beta$</td><td>偏袒的净效应</td><td>核心待估参数</td></tr>
</tbody>
</table>

<h4>第六步　稳健性</h4>
<p>四项。只保留族群边界附近的像素。按制度质量分组。把夜光换成人口密度。排除首都所在区域。<strong>第一项与第四项最关键：前者排除族群间的地理差异，后者排除首都的政治集聚。</strong></p>

<h4>第七步　复制要点</h4>
<p>三层固定效应最容易写错。判断标准是：<strong>处理变量的变动必须来自某个固定效应没有吸收的维度。</strong>若 $D$ 只随族群与年变化，则 $\\delta_{et}$ 会把它全部吸收，模型无法识别。</p>
</div>

"""

s = s[:a] + NEW + s[b:]
io.open(P, "w", encoding="utf-8").write(s)
print("case4 rewritten, len", len(s))
