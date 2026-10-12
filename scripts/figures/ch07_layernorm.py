"""배치 정규화(노드마다 따로)와 레이어 정규화(층 전체를 한 번에)를 노드 그림으로 비교한 PNG를 만든다.

배치 정규화는 노드 하나의 값을 샘플들에 걸쳐, 레이어 정규화는 샘플 하나의 값을 노드들에 걸쳐
평균과 분산을 구한다. 그래서 정규화 모듈이 노드마다 하나씩 있는지, 층에 하나인지가 다르다.

실행: python3 scripts/figures/ch07_layernorm.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from ch05_sigmoid_animation import set_korean_font

OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06/layernorm-vs-batchnorm.png"
CURVE = "#315f7d"
ORANGE = "#e87924"
DARK = "#334155"
GRAY = "#94a3b8"
R = 0.42
YS = [1.7, 0.0, -1.7]
GAP_SUM_MOD, GAP_MOD_ACT = 2.0, 4.0  # 가중합 노드 기준 모듈·활성화 노드의 x 위치
MOD_W = 1.7


def node(ax, x, y, text):
    ax.add_patch(Circle((x, y), R, fc="white", ec=CURVE, lw=2.4, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=17, color=CURVE, zorder=4)


def arrow(ax, x0, x1, y):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=15,
                                 color=GRAY, lw=1.8, shrinkA=0, shrinkB=0, zorder=2))


def module(ax, cx, cy, h, text):
    ax.add_patch(FancyBboxPatch((cx - MOD_W / 2, cy - h / 2), MOD_W, h,
                                boxstyle="round,pad=0.02,rounding_size=0.3",
                                fc="#fff4e8", ec=ORANGE, lw=2.4, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=14, fontweight="bold",
            color=ORANGE, linespacing=1.35, zorder=4)


def panel(ax, x0, subtitle, per_node):
    x_mod, x_act = x0 + GAP_SUM_MOD, x0 + GAP_MOD_ACT
    for y in YS:
        node(ax, x0, y, "Σ")
        node(ax, x_act, y, "f")
        arrow(ax, x0 + R, x_mod - MOD_W / 2 - 0.02, y)
        arrow(ax, x_mod + MOD_W / 2 + 0.02, x_act - R, y)
        if per_node:
            module(ax, x_mod, y, 0.95, "배치\n정규화")
    if not per_node:
        module(ax, x_mod, 0.0, 4.5, "레이어\n정규화")
    ax.text(x_mod, 3.2, subtitle, ha="center", va="center", fontsize=13, color=DARK)


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(11.0, 5.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
    ax.set_aspect("equal")
    ax.set(xlim=(-1.0, 12.8), ylim=(-2.9, 3.8))
    ax.axis("off")

    panel(ax, 0.0, "노드마다 따로, 샘플들에 걸쳐", per_node=True)
    panel(ax, 7.4, "층 전체를 한 번에, 한 샘플의 노드들에 걸쳐", per_node=False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
