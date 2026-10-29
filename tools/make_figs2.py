# -*- coding: utf-8 -*-
"""第二版新增示意图。"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Rectangle

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "path"

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fig")
INK, BLUE, RED, GREEN, GREY, GOLD = "#1c2434", "#2f5fb3", "#b3322f", "#2e7d5b", "#8a93a6", "#b8860b"


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print("ok", name, os.path.getsize(p))


def node(ax, x, y, w, h, text, fc="#eef2fb", ec=BLUE, fs=11, bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.09",
                                linewidth=1.3, edgecolor=ec, facecolor=fc, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            fontweight="bold" if bold else "normal", zorder=4)


def arrow(ax, p, q, color=INK, lw=1.3, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13, linewidth=lw,
                                 color=color, connectionstyle=f"arc3,rad={rad}",
                                 zorder=2, linestyle=ls))


# ------------------------------------------------------- 方法难度阶梯
def fig_ladder():
    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    ax.set_xlim(0, 11.6); ax.set_ylim(0, 10); ax.axis("off")
    steps = [
        (1, "描述与\n多元回归", "#dfe6f5", BLUE),
        (2, "固定效应\n与双重差分", "#cfdcf0", BLUE),
        (3, "工具变量\n断点\n合成控制", "#bcd0ea", GREEN),
        (4, "网络模型\n结构模型\n机器学习", "#a9c3e2", GOLD),
        (5, "异质性稳健\n估计与\n空间推断", "#95b6da", RED),
    ]
    for i, (lvl, name, fc, ec) in enumerate(steps):
        x0 = 0.5 + i * 2.2
        h = 1.7 + i * 1.45
        ax.add_patch(Rectangle((x0, 1.0), 1.9, h, facecolor=fc, edgecolor="white",
                               linewidth=2, zorder=2))
        ax.text(x0 + 0.95, 1.0 + h - 0.55, "第 %d 级" % lvl, ha="center", va="top",
                fontsize=11, color=ec, fontweight="bold", zorder=3)
        ax.text(x0 + 0.95, 1.0 + h / 2 - 0.45, name, ha="center", va="center",
                fontsize=9.5, color=INK, zorder=3, linespacing=1.65)
    ax.annotate("", xy=(11.2, 0.62), xytext=(0.6, 0.62),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4))
    ax.text(5.8, 0.18, "外生信息的来源越来越远，假设也越来越难以直接检验",
            ha="center", fontsize=10, color=GREY)
    fig.tight_layout()
    save(fig, "fig-ladder.svg")


# ------------------------------------------------------- 制裁的选择问题
def fig_sanctions():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis("off")
    node(ax, 2.4, 6.6, 3.0, 1.3, "被制裁国的\n行为 $X$", fc="#fbeef0", ec=RED)
    node(ax, 6.0, 6.6, 3.0, 1.3, "是否被制裁\n$S$", fc="#eef2fb", ec=BLUE)
    node(ax, 9.6, 6.6, 3.0, 1.3, "结果变量\n$Y$", fc="#eef2fb", ec=BLUE)
    node(ax, 6.0, 2.2, 3.4, 1.4, "战略价值与\n盟友关系 $U$", fc="#f3f3f3", ec=GREY)

    arrow(ax, (3.9, 6.6), (4.5, 6.6), color=RED)
    arrow(ax, (7.5, 6.6), (8.1, 6.6), color=BLUE)
    arrow(ax, (5.2, 2.9), (5.2, 5.9), color=GREY)
    arrow(ax, (6.9, 2.9), (9.3, 5.9), color=GREY)
    ax.text(4.28, 4.70, "选择偏差", ha="center", fontsize=10, color=RED)
    ax.text(2.4, 5.5, "反向因果", ha="center", fontsize=10, color=RED)
    ax.text(6.0, 8.55, "制裁不是随机分配的", ha="center", fontsize=11.5, color=INK, fontweight="bold")
    fig.tight_layout()
    save(fig, "fig-sanctions.svg")


# ------------------------------------------------------- 合成控制
def fig_synthetic():
    rng = np.random.default_rng(9)
    t = np.arange(0, 40)
    treat = np.zeros_like(t, dtype=float)
    base = 10 + 0.30 * t + rng.normal(0, 0.12, t.size)
    synth = base + rng.normal(0, 0.08, t.size)
    actual = base.copy()
    actual[25:] += np.linspace(0, -3.2, 15)
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.plot(t[:25], actual[:25], color=RED, lw=2.6, label="处理单元：实际轨迹")
    ax.plot(t[24:], actual[24:], color=RED, lw=2.6)
    ax.plot(t, synth, color=INK, lw=1.8, ls="--", label="合成对照：加权组合")
    ax.axvline(24.5, color=GREY, lw=1.4, ls=(0, (4, 3)))
    ax.fill_between(t[25:], synth[25:], actual[25:], color=RED, alpha=0.12)
    ax.annotate("效应", xy=(33, (synth[33] + actual[33]) / 2), fontsize=12, color=RED)
    ax.set_xlabel("时间", fontsize=11)
    ax.set_ylabel("结果变量 $Y$", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(fontsize=9.5, frameon=False, loc="lower left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "fig-synthetic.svg")


# ------------------------------------------------------- 网络等级
def fig_hierarchy():
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    rng = np.random.default_rng(13)
    hub = [(5.0, 5.0)]
    ring = [(5 + 2.6 * np.cos(a), 5 + 2.6 * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 6, endpoint=False)]
    outer = [(5 + 4.2 * np.cos(a), 5 + 4.2 * np.sin(a)) for a in np.linspace(0.3, 2 * np.pi, 10, endpoint=False)]
    pts = hub + ring + outer
    for p in ring:
        ax.plot([5.0, p[0]], [5.0, p[1]], color="#c3cad9", lw=1.6, zorder=1)
    for i, p in enumerate(outer):
        for q in ring[i % 6:i % 6 + 2]:
            ax.plot([p[0], q[0]], [p[1], q[1]], color="#dde1ea", lw=1.0, zorder=1)
    ax.scatter([p[0] for p in outer], [p[1] for p in outer], s=80, color="#aeb9d0", zorder=3,
               edgecolor="white", linewidth=1.1)
    ax.scatter([p[0] for p in ring], [p[1] for p in ring], s=170, color=BLUE, zorder=4,
               edgecolor="white", linewidth=1.3)
    ax.scatter([5.0], [5.0], s=420, color=RED, zorder=5, edgecolor="white", linewidth=1.6)
    ax.text(5.0, 4.25, "枢纽", ha="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(8.3, 8.4, "外围", fontsize=10.5, color=GREY)
    ax.annotate("", xy=(8.05, 8.2), xytext=(7.2, 7.4),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    ax.text(5.0, 0.5, "度数越高，越处在网络的结构位置之上", ha="center", fontsize=10, color=INK)
    fig.tight_layout()
    save(fig, "fig-hierarchy.svg")


# ------------------------------------------------------- 份额移动
def fig_shiftshare():
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    node(ax, 2.0, 7.4, 2.9, 1.3, "事前份额\n$s_{ik}$", fc="#e8f4ee", ec=GREEN)
    node(ax, 2.0, 3.0, 2.9, 1.3, "外部冲击\n$g_{kt}$", fc="#e8f4ee", ec=GREEN)
    node(ax, 5.4, 5.2, 2.6, 1.3, "暴露度\n$E_{it}$", fc="#eef2fb", ec=BLUE)
    node(ax, 8.6, 5.2, 2.4, 1.3, "结果\n$Y_{it}$", fc="#fbeef0", ec=RED)
    ax.text(5.4, 3.4, "$E_{it}=\\sum_k s_{ik}\\,g_{kt}$", ha="center", fontsize=12.5, color=INK)
    arrow(ax, (3.4, 7.0), (4.6, 5.8), color=GREEN)
    arrow(ax, (3.4, 3.4), (4.6, 4.6), color=GREEN)
    arrow(ax, (6.7, 5.2), (7.4, 5.2), color=BLUE)
    ax.text(2.0, 5.2, "两项相乘", ha="center", fontsize=10, color=GREY)
    ax.text(5.0, 9.4, "份额固定，冲击外生，只有乘积随时间与单元变动",
            ha="center", fontsize=10.5, color=INK)
    fig.tight_layout()
    save(fig, "fig-shiftshare.svg")


if __name__ == "__main__":
    fig_ladder()
    fig_sanctions()
    fig_synthetic()
    fig_hierarchy()
    fig_shiftshare()
