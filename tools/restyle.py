# -*- coding: utf-8 -*-
"""重排目录与标题的视觉层级，并为拆解区块设定轻量排版。"""
import io

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\assets\style.css"
c = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 目录
old_toc = """.toc{list-style:none;margin:0;padding:0;font-size:13.5px;line-height:1.65;}
.toc>li{margin:2px 0;}
.toc a{
  display:block;padding:5px 10px;border-radius:5px;
  color:var(--ink-soft);text-decoration:none;
  border-left:2px solid transparent;
  transition:background .15s,color .15s,border-color .15s;
}
.toc a:hover{background:#f0f2f7;color:var(--blue);}
.toc a.active{background:var(--blue-wash);color:var(--blue);border-left-color:var(--blue);font-weight:600;}
.toc .sub{margin:2px 0 6px 10px;list-style:none;padding:0;font-size:12.5px;}
.toc .sub a{padding:3px 8px;color:var(--grey);}"""

new_toc = """/* 三级目录：一级粗体带色条，二级与三级逐级缩进并以细线串联 */
.toc{list-style:none;margin:0;padding:0;line-height:1.5;}
.toc a{text-decoration:none;display:block;border-radius:0 5px 5px 0;
  transition:background .15s,color .15s,border-color .15s;}
.toc>li.lv1{margin:7px 0 1px;}
.toc>li.lv1>a{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:12.8px;font-weight:700;color:var(--ink);
  padding:6px 8px 6px 11px;
  border-left:3px solid #d6dbe6;
  letter-spacing:.01em;
}
.toc>li.lv1>a:hover{border-left-color:var(--blue);background:#f3f5fa;}
.toc>li.lv1>a.active{border-left-color:var(--blue);background:var(--blue-wash);color:var(--blue);}
.toc .sub{
  list-style:none;margin:3px 0 9px;padding:1px 0 1px 13px;
  border-left:1px solid #e6e9f1;
}
.toc .sub .lv2>a{
  font-size:11.8px;color:var(--ink-soft);
  padding:3px 8px 3px 9px;border-left:2px solid transparent;
}
.toc .sub .lv2>a:hover{color:var(--blue);border-left-color:#c3cfe8;}
.toc .sub .lv3>a{
  font-size:11.2px;color:#7a8398;
  padding:2px 8px 2px 20px;border-left:2px solid transparent;
}
.toc .sub .lv3>a:hover{color:var(--blue);border-left-color:#cdd7ec;}
.toc .sub a.active{color:var(--blue);background:var(--blue-wash);border-left-color:var(--blue);}"""

assert old_toc in c, "目录样式未命中"
c = c.replace(old_toc, new_toc, 1)

# ---------------------------------------------------------------- 标题竖线
old_h2 = """h2{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:25px;line-height:1.5;font-weight:700;
  margin:34px 0 22px;
  padding-bottom:14px;
  border-bottom:2px solid var(--ink);
  letter-spacing:.01em;
}"""
new_h2 = """h2{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:25px;line-height:1.5;font-weight:700;
  margin:34px 0 22px;
  padding:2px 0 14px 16px;
  border-left:7px solid var(--ink);
  border-bottom:2px solid var(--ink);
  letter-spacing:.01em;
}"""
assert old_h2 in c
c = c.replace(old_h2, new_h2, 1)

old_h3 = """h3{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:18.5px;font-weight:700;line-height:1.6;
  margin:44px 0 14px;color:var(--ink);
}
h3::before{content:"";display:inline-block;width:3px;height:17px;background:var(--gold);
  margin-right:10px;vertical-align:-2px;border-radius:1px;}"""
new_h3 = """h3{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:18px;font-weight:700;line-height:1.6;
  margin:44px 0 14px;color:var(--ink);
  padding:2px 0 2px 13px;
  border-left:4px solid var(--blue);
}
h3::before{content:none;}"""
assert old_h3 in c
c = c.replace(old_h3, new_h3, 1)

old_h4 = """h4{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:15.5px;font-weight:700;margin:30px 0 10px;color:var(--ink-soft);
}"""
new_h4 = """h4{
  font-family:"Microsoft YaHei","PingFang SC",sans-serif;
  font-size:15px;font-weight:700;margin:30px 0 10px;color:var(--ink-soft);
  padding:1px 0 1px 11px;
  border-left:4px solid var(--gold);
}"""
assert old_h4 in c
c = c.replace(old_h4, new_h4, 1)

# ---------------------------------------------------------------- 拆解区块
anchor = "/* ---------------- 响应式 ---------------- */"
trace_css = """/* ---------------- 文献拆解区块 ----------------
   字号更小、行距更松、色彩更淡；只有加粗的判定句与标签使用强调色。 */
.trace{
  margin:6px 0 26px -4px;
  padding:2px 0 2px 16px;
  border-left:1px dashed #e3e7f0;
}
.trace h4{font-size:14.2px;margin:26px 0 9px;border-left-width:3px;}
.trace p{
  font-size:14.6px;line-height:1.95;color:#3a4254;
  margin:0 0 15px;text-align:justify;
}
.trace strong{
  font-weight:700;color:#1b4fa8;background:none;
}
.trace table{font-size:12.4px;}
.trace table th{font-size:12px;padding:8px 9px;}
.trace table td{padding:7px 9px;}
.trace table caption{font-size:11.6px;}
.trace .eq{margin:18px 0;padding:12px 54px 12px 16px;background:#fcfcfe;}
.trace .eqno{top:13px;font-size:11.5px;}
.trace mjx-container{font-size:100%;}

"""
assert anchor in c
c = c.replace(anchor, trace_css + anchor, 1)

io.open(P, "w", encoding="utf-8").write(c)
print("css ok", len(c))
