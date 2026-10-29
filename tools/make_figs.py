# -*- coding: utf-8 -*-
"""生成技术文档所需的示意图（SVG，文字转路径，跨机器显示一致）。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Rectangle, Polygon

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "path"

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fig")
os.makedirs(OUT, exist_ok=True)

INK = "#1c2434"
BLUE = "#2f5fb3"
RED = "#b3322f"
GREEN = "#2e7d5b"
GREY = "#8a93a6"
GOLD = "#b8860b"


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("ok", name, os.path.getsize(p))


def node(ax, x, y, w, h, text, fc="#eef2fb", ec=BLUE, fs=12, bold=False):
    b = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.10",
                       linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=3)
    ax.add_patch(b)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            fontweight="bold" if bold else "normal", zorder=4)


def arrow(ax, p, q, color=INK, lw=1.4, style="-|>", rad=0.0, ls="-"):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=14, linewidth=lw,
                        color=color, connectionstyle=f"arc3,rad={rad}", zorder=2, linestyle=ls)
    ax.add_patch(a)


# ---------------------------------------------------------------- 图 1 三个混淆源
def fig_confound():
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    ax = axes[0]
    node(ax, 5, 2.2, 3.0, 1.5, "干预\n$D$", fc="#eef2fb")
    node(ax, 5, 7.8, 3.0, 1.5, "结果\n$Y$", fc="#fbeef0", ec=RED)
    node(ax, 1.9, 5.0, 3.0, 1.5, "混淆变量\n$U$", fc="#f3f3f3", ec=GREY)
    arrow(ax, (5, 3.0), (5, 7.0))
    arrow(ax, (2.6, 5.9), (3.7, 7.1), color=GREY)
    arrow(ax, (2.6, 4.1), (3.7, 2.9), color=GREY)
    ax.set_title("遗漏变量", fontsize=13, color=INK, pad=6)

    ax = axes[1]
    node(ax, 2.6, 5.0, 3.0, 1.5, "干预\n$D$", fc="#eef2fb")
    node(ax, 7.4, 5.0, 3.0, 1.5, "结果\n$Y$", fc="#fbeef0", ec=RED)
    arrow(ax, (4.2, 5.7), (5.8, 5.7), color=BLUE)
    arrow(ax, (5.8, 4.3), (4.2, 4.3), color=RED, rad=0.0)
    ax.text(5.0, 6.4, "想估计的", ha="center", fontsize=10, color=BLUE)
    ax.text(5.0, 3.2, "真实的", ha="center", fontsize=10, color=RED)
    ax.set_title("反向因果", fontsize=13, color=INK, pad=6)

    ax = axes[2]
    rng = np.random.default_rng(17)
    xs = rng.uniform(0.8, 9.2, 400)
    ys = 0.55 * xs + 2.6 + rng.normal(0, 0.85, 400)
    keep = ys > 6.4
    ax.scatter(xs[keep], ys[keep], s=13, color=BLUE, alpha=0.8, edgecolor="none", zorder=3)
    ax.scatter(xs[~keep], ys[~keep], s=13, color="#d9dde8", alpha=0.9, edgecolor="none", zorder=2)
    ax.axhline(6.4, color=RED, lw=1.6, ls="--", zorder=4)
    ax.text(0.5, 6.75, "可观测门槛", fontsize=10, color=RED)
    ax.text(0.5, 2.0, "被剔除的样本\n（看不见）", fontsize=10, color=GREY)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_title("样本选择", fontsize=13, color=INK, pad=6)

    fig.tight_layout()
    save(fig, "fig-confound.svg")


# ---------------------------------------------------------------- 图 2 点线面
def fig_point_line_area():
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    for i in range(1, 10):
        ax.plot([0, 10], [i, i], color="#e6e9f2", lw=0.8, zorder=0)
        ax.plot([i, i], [0, 10], color="#e6e9f2", lw=0.8, zorder=0)

    roads = [([0.4, 7.6], [3.2, 8.4]), ([3.2, 8.4], [6.6, 6.2]), ([6.6, 6.2], [9.6, 6.8]),
             ([1.2, 3.0], [4.4, 4.6]), ([4.4, 4.6], [6.6, 6.2]), ([4.4, 4.6], [8.0, 3.2])]
    for (p, q) in roads:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=3.4, solid_capstyle="round", zorder=2,
                alpha=0.85)

    rng = np.random.default_rng(7)
    pts = rng.uniform(0.7, 9.3, size=(26, 2))
    ax.scatter(pts[:, 0], pts[:, 1], s=44, color=RED, zorder=4, edgecolor="white", linewidth=1.1)

    ax.add_patch(Rectangle((6.6, 6.2), 1.9, 1.9, facecolor=BLUE, alpha=0.14, edgecolor=BLUE,
                           lw=1.4, zorder=1))
    ax.text(7.55, 8.35, "3 km 缓冲区", ha="center", fontsize=10, color=BLUE)

    ax.annotate("点\n村庄、矿点、水电站", xy=(2.25, 4.05), xytext=(1.0, 2.1), fontsize=11,
                color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.annotate("线\n公路、铁路、界河、行政边界", xy=(7.95, 6.28), xytext=(4.6, 1.4), fontsize=11,
                color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.annotate("面\n网格、县、族群家园", xy=(9.5, 9.5), xytext=(5.9, 9.3), fontsize=11,
                color=GREY, arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    fig.tight_layout()
    save(fig, "fig-point-line-area.svg")


# ---------------------------------------------------------------- 图 3 DID
def fig_did():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    t = [0, 1]
    ax.plot(t, [3.0, 4.2], "-o", color=BLUE, lw=2.4, ms=8, label="处理组：实际轨迹")
    ax.plot(t, [3.0, 7.4], "--o", color=BLUE, lw=1.6, ms=6, mfc="white", label="处理组：无干预反事实")
    ax.plot(t, [2.2, 3.4], "-s", color=GREY, lw=2.4, ms=8, label="对照组：实际轨迹")
    ax.annotate("", xy=(1.0, 7.2), xytext=(1.0, 4.4),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
    ax.text(1.04, 5.8, "$\\hat{\\beta}_{\\mathrm{DID}}$", fontsize=15, color=RED)
    ax.text(1.04, 2.9, "共同趋势", fontsize=10, color=GREY, ha="left")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["干预前", "干预后"], fontsize=11)
    ax.set_yticks([])
    ax.set_xlim(-0.16, 1.45)
    ax.set_ylabel("结果变量 $Y$", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    fig.tight_layout()
    save(fig, "fig-did.svg")


# ---------------------------------------------------------------- 图 4 空间断点
def fig_rd():
    rng = np.random.default_rng(3)
    n = 220
    x = rng.uniform(-1, 1, n)
    jump = 2.1
    y = 1.6 * x + 3.2 + jump * (x > 0) + rng.normal(0, 0.95, n)
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    ax.scatter(x[x <= 0], y[x <= 0], s=16, color=GREY, alpha=0.75, edgecolor="none")
    ax.scatter(x[x > 0], y[x > 0], s=16, color=BLUE, alpha=0.75, edgecolor="none")

    z = x[x <= 0]; ax.plot([-1, 0], [np.polyval(np.polyfit(z, y[x <= 0], 1), -1),
                                    np.polyval(np.polyfit(z, y[x <= 0], 1), 0)],
                           color=GREY, lw=2.6)
    z = x[x > 0]; ax.plot([0, 1], [np.polyval(np.polyfit(z, y[x > 0], 1), 0),
                                   np.polyval(np.polyfit(z, y[x > 0], 1), 1)],
                          color=BLUE, lw=2.6)
    ax.axvline(0, color=RED, lw=1.8, ls="--")
    ax.annotate("", xy=(0, 5.05), xytext=(0, 3.15),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.8))
    ax.text(0.035, 4.1, "$\\tau$", fontsize=16, color=RED)
    ax.set_xlim(-1.10, 1.10); ax.set_ylim(-1.0, 9.2)
    ax.text(0.0, 8.6, "断点：边界、河流、海拔阈值", ha="center", fontsize=10, color=RED)
    ax.set_xlabel("到断点的距离（或断点变量）", fontsize=11)
    ax.set_ylabel("结果变量 $Y$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "fig-rd.svg")


# ---------------------------------------------------------------- 图 5 IV
def fig_iv():
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    node(ax, 1.7, 7.2, 2.6, 1.4, "工具变量\n$Z$", fc="#e8f4ee", ec=GREEN)
    node(ax, 5.0, 7.2, 2.6, 1.4, "内生干预\n$D$", fc="#eef2fb", ec=BLUE)
    node(ax, 8.3, 7.2, 2.6, 1.4, "结果\n$Y$", fc="#fbeef0", ec=RED)
    node(ax, 5.0, 2.2, 2.9, 1.4, "不可观测因素\n$U$", fc="#f3f3f3", ec=GREY)

    arrow(ax, (3.1, 7.2), (3.6, 7.2), color=GREEN, lw=2.2)
    arrow(ax, (6.4, 7.2), (6.9, 7.2), color=BLUE, lw=2.2)
    arrow(ax, (5.0, 3.0), (5.0, 6.4), color=GREY, lw=1.6)
    arrow(ax, (6.3, 3.0), (7.9, 6.4), color=GREY, lw=1.6)

    arrow(ax, (1.7, 7.95), (8.3, 7.95), color=RED, lw=1.4, ls=(0, (5, 3)), rad=-0.42)
    ax.plot([5.0], [9.02], marker="x", ms=13, mew=2.6, color=RED, zorder=6)
    ax.text(5.0, 9.42, "禁止通行：违背排除限制", ha="center", fontsize=10.5, color=RED)

    ax.text(3.30, 5.55, "第一阶段\n须显著", ha="center", fontsize=9.5, color=GREEN)
    ax.text(6.55, 5.55, "被估计的\n因果效应", ha="center", fontsize=9.5, color=BLUE)
    ax.text(3.30, 3.95, "混淆渠道", ha="left", fontsize=9.5, color=GREY)
    fig.tight_layout()
    save(fig, "fig-iv.svg")


# ---------------------------------------------------------------- 图 6 可达性网络
def fig_market_access():
    rng = np.random.default_rng(4)
    gx, gy = np.meshgrid(np.linspace(1.2, 8.8, 5), np.linspace(1.2, 8.8, 4))
    xy = np.column_stack([gx.ravel(), gy.ravel()]) + rng.normal(0, 0.42, size=(20, 2))
    xy[3] = [1.9, 6.0]
    n = len(xy)
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    edges = set()
    for i in range(n):
        d = np.linalg.norm(xy - xy[i], axis=1)
        for j in np.argsort(d)[1:3]:
            edges.add(tuple(sorted((i, int(j)))))
    for (i, j) in edges:
        ax.plot([xy[i, 0], xy[j, 0]], [xy[i, 1], xy[j, 1]], color="#c8cfdd", lw=1.4, zorder=1)

    start = int(np.argmin(xy[:, 0] + xy[:, 1]))
    market = int(np.argmax(xy[:, 0] + xy[:, 1]))

    import heapq
    adj = {i: [] for i in range(n)}
    for (i, j) in edges:
        w = float(np.linalg.norm(xy[i] - xy[j]))
        adj[i].append((j, w)); adj[j].append((i, w))
    dist = {i: float("inf") for i in range(n)}
    prev = {i: None for i in range(n)}
    dist[start] = 0.0
    pq = [(0.0, start)]
    while pq:
        d0, u = heapq.heappop(pq)
        if d0 > dist[u]:
            continue
        for (v, w) in adj[u]:
            if d0 + w < dist[v]:
                dist[v] = d0 + w
                prev[v] = u
                heapq.heappush(pq, (d0 + w, v))
    path = []
    cur = market
    while cur is not None:
        path.append(cur); cur = prev[cur]
    path.reverse()
    for a, b in zip(path[:-1], path[1:]):
        ax.plot([xy[a, 0], xy[b, 0]], [xy[a, 1], xy[b, 1]], color=RED, lw=3.2, zorder=3,
                solid_capstyle="round")

    ax.scatter(xy[:, 0], xy[:, 1], s=170, color=BLUE, zorder=4, edgecolor="white", linewidth=1.4)
    ax.scatter(xy[path, 0], xy[path, 1], s=200, color=RED, zorder=5, edgecolor="white", linewidth=1.6)
    ax.text(xy[market, 0] + 0.28, xy[market, 1] + 0.30, "市场（城市）", fontsize=11, color=RED)
    ax.text(xy[start, 0] + 0.28, xy[start, 1] - 0.42, "起点村庄", fontsize=11, color=RED)
    ax.text(5.0, 0.25, "市场准入 $=$ 各市场规模按运输成本加权求和",
            ha="center", fontsize=10.5, color=INK)
    fig.tight_layout()
    save(fig, "fig-market-access.svg")


# ---------------------------------------------------------------- 图 7 夜光与 GDP
def fig_ntl():
    rng = np.random.default_rng(21)
    n = 130
    lny = rng.uniform(6.4, 11.2, n)
    lnl = 0.92 * lny - 4.6 + rng.normal(0, 0.62, n)
    fig, ax = plt.subplots(figsize=(6.3, 4.3))
    ax.scatter(lny, lnl, s=24, color=BLUE, alpha=0.72, edgecolor="none")
    b, a = np.polyfit(lny, lnl, 1)
    xs = np.linspace(6.2, 11.4, 50)
    ax.plot(xs, a + b * xs, color=RED, lw=2.2)
    ax.text(6.6, 6.7, f"斜率 $\\hat\\beta={b:.2f}$", fontsize=13, color=RED)
    ax.set_xlabel("人均 GDP 的对数 $\\ln Y$", fontsize=11)
    ax.set_ylabel("夜光强度的对数 $\\ln L$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "fig-ntl.svg")


# ---------------------------------------------------------------- 图 8 网络中心性
def fig_network():
    rng = np.random.default_rng(5)
    n = 26
    ang = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    xy = []
    for c in zip(np.cos(ang) * 2.6 + 5, np.sin(ang) * 2.6 + 5):
        xy.append(c)
    for k in range(n - 5):
        a = rng.uniform(0, 2 * np.pi); r = rng.uniform(0.2, 1.0)
        xy.append((5 + np.cos(a) * r * 2.4, 5 + np.sin(a) * r * 2.4))
    xy = np.array(xy)

    fig, ax = plt.subplots(figsize=(6.0, 5.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    edges = set()
    for i in range(5):
        for j in range(i + 1, 5):
            edges.add((i, j))
    for i in range(5, n):
        d = np.linalg.norm(xy[:5] - xy[i], axis=1)
        for j in np.argsort(d)[:2]:
            edges.add((i, int(j)))
    for (i, j) in edges:
        ax.plot([xy[i, 0], xy[j, 0]], [xy[i, 1], xy[j, 1]], color="#c3cad9", lw=1.2, zorder=1)
    deg = np.zeros(n)
    for (i, j) in edges:
        deg[i] += 1; deg[j] += 1
    ax.scatter(xy[:, 0], xy[:, 1], s=30 + deg ** 1.9 * 26, color=BLUE, alpha=0.85,
               edgecolor="white", linewidth=1.3, zorder=3)
    top = int(np.argmax(deg))
    ax.scatter([xy[top, 0]], [xy[top, 1]], s=30 + deg[top] ** 1.9 * 26, color=RED,
               edgecolor="white", linewidth=1.6, zorder=4)
    ax.text(xy[top, 0], xy[top, 1] + 0.55, "中心性最高", fontsize=11, color=RED, ha="center")
    ax.text(5.0, 0.2, "圆圈越大，该节点的度中心性越高", ha="center", fontsize=10.5, color=INK)
    fig.tight_layout()
    save(fig, "fig-network.svg")


# ---------------------------------------------------------------- 图 9 事件研究
def fig_event():
    k = np.arange(-4, 6)
    est = np.array([0.08, -0.05, 0.11, -0.02, 0.00, 0.34, 0.51, 0.63, 0.70, 0.74])
    se = np.array([0.15, 0.14, 0.13, 0.12, 0.00, 0.14, 0.15, 0.16, 0.17, 0.19])
    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    ax.axhline(0, color=GREY, lw=1.0, ls=(0, (4, 3)))
    ax.axvline(-0.5, color=RED, lw=1.4, ls="--")
    ax.errorbar(k, est, yerr=1.96 * se, fmt="o", color=BLUE, ms=6, lw=1.6,
                capsize=4, ecolor=BLUE, alpha=0.95)
    ax.set_xlabel("相对政策实施期的年数 $k$", fontsize=11)
    ax.set_ylabel("效应估计 $\\hat\\beta_k$", fontsize=11)
    ax.set_xticks(k)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(-3.6, 1.0, "政策前系数应贴近 0\n否则共同趋势不成立", fontsize=9.5, color=RED)
    fig.tight_layout()
    save(fig, "fig-event.svg")


# ---------------------------------------------------------------- 图 10 决策树
def fig_tree():
    fig, ax = plt.subplots(figsize=(9.6, 6.2))
    ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis("off")
    node(ax, 8, 9.0, 6.4, 1.1, "外生变动来自哪里", fc="#1c2434", ec="#1c2434", fs=13, bold=True)
    ax.texts[-1].set_color("white")

    items = [
        (2.6, "有一条画在纸上的线\n（边界、河流、海拔）", "断点回归", RED, "案例 1"),
        (8.0, "有一份时间表或工程规划\n（分期、批次、路线）", "双重差分", BLUE, "案例 2、4、5"),
        (13.4, "有一个只影响干预\n不影响结果的推力", "工具变量", GREEN, "案例 3"),
    ]
    for (x, txt, tag, col, cas) in items:
        node(ax, x, 6.2, 4.2, 1.5, txt, fc="#f7f8fc")
        arrow(ax, (8, 8.4), (x, 7.1))
        node(ax, x, 2.6, 3.0, 1.2, tag, fc="white", ec=col, fs=13, bold=True)
        arrow(ax, (x, 5.4), (x, 3.2), color=col)
        ax.text(x, 1.5, cas, ha="center", fontsize=9.5, color=GREY)
    fig.tight_layout()
    save(fig, "fig-tree.svg")


# ---------------------------------------------------------------- 图 11 空间相关
def fig_spatial_se():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4))
    rng = np.random.default_rng(31)
    for ax, radius, title in zip(axes, [0.0, 1.15], ["独立抽样", "空间相关"]):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
        c = np.array([[2.6, 7.2], [5.0, 7.4], [7.4, 7.0], [2.8, 4.4], [5.2, 4.6],
                      [7.6, 4.2], [3.0, 1.6], [5.4, 1.5], [7.8, 1.8]])
        if radius > 0:
            for p in c:
                ax.add_patch(Circle(p, radius, facecolor=BLUE, alpha=0.10, edgecolor="none"))
            base = np.array([0.35, 0.25])
            vals = base + rng.normal(0, 0.04, size=(9, 2))
            vals[3:6] = base + 0.16 + rng.normal(0, 0.03, size=(3, 2))
        else:
            vals = rng.uniform(0.15, 0.45, size=(9, 1)) * np.array([1, 0.7]) + 0.2
        ax.scatter(c[:, 0], c[:, 1], s=95, color=BLUE, zorder=3, edgecolor="white", linewidth=1.3)
        ax.set_title(title, fontsize=12, color=INK)
    axes[0].text(5, -0.6, "扰动互不相关：常规标准误可用", ha="center", fontsize=10, color=GREY)
    axes[1].text(5, -0.6, "相邻单元的扰动同起同落：须用聚类或空间标准误",
                 ha="center", fontsize=10, color=RED)
    fig.tight_layout()
    save(fig, "fig-spatial-se.svg")


if __name__ == "__main__":
    fig_confound()
    fig_point_line_area()
    fig_did()
    fig_rd()
    fig_iv()
    fig_market_access()
    fig_ntl()
    fig_network()
    fig_event()
    fig_tree()
    fig_spatial_se()
    print("done")
