"""노드 하나의 활성화 함수 뒤에 드롭아웃을 붙이고, 살릴 확률 p로 출력이 갈리는 PNG를 만든다.

실행: python3 scripts/figures/ch08_dropout_node.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch07/dropout-node.png"
BLACK = "#222222"
GRAY = "#94a3b8"
R = 0.42
BOX_W, BOX_H = 2.0, 0.9

X_IN, X_SUM, X_ACT, X_DROP, X_OUT = 0.0, 3.0, 5.0, 7.4, 10.4
INPUTS = [1.5, 0.0, -1.5]
Y_KEEP, Y_DROP = 1.2, -1.2


def node(ax, x, y, text, ls="-"):
    ax.add_patch(Circle((x, y), R, fc="white", ec=BLACK, lw=2.4, ls=ls, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=17, color=BLACK, zorder=4)


def arrow(ax, p, q, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=BLACK,
                                 lw=1.8, ls=ls, shrinkA=0, shrinkB=0, zorder=2))


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(9.4, 3.9), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
    ax.set_aspect("equal")
    ax.set(xlim=(-0.9, 12.0), ylim=(-2.4, 2.9))
    ax.axis("off")

    for i, y in enumerate(INPUTS, start=1):
        ax.plot([X_IN + R, X_SUM - R], [y, 0], color=GRAY, lw=1.3, zorder=1)
        node(ax, X_IN, y, f"$x_{i}$")
    node(ax, X_SUM, 0, "Σ")
    arrow(ax, (X_SUM + R, 0), (X_ACT - R, 0))
    node(ax, X_ACT, 0, "f")
    arrow(ax, (X_ACT + R, 0), (X_DROP - BOX_W / 2 - 0.02, 0))
    ax.text((X_ACT + X_DROP - BOX_W / 2) / 2, 0.3, "a", ha="center", va="center", fontsize=15, color=BLACK)

    ax.add_patch(FancyBboxPatch((X_DROP - BOX_W / 2, -BOX_H / 2), BOX_W, BOX_H,
                                boxstyle="round,pad=0.02,rounding_size=0.25",
                                fc="white", ec=BLACK, lw=2.4, zorder=2))
    ax.text(X_DROP, 0, "드롭아웃", ha="center", va="center", fontsize=14, fontweight="bold",
            color=BLACK, zorder=4)
    ax.text(X_DROP, BOX_H / 2 + 0.35, "살릴 확률 p", ha="center", va="center", fontsize=14, color=BLACK)

    # 확률 p로 출력 a를 그대로 넘기고, 확률 1-p로 0을 넘긴다
    x0 = X_DROP + BOX_W / 2 + 0.02
    arrow(ax, (x0, 0.15), (X_OUT - R, Y_KEEP))
    arrow(ax, (x0, -0.15), (X_OUT - R, Y_DROP), ls="--")
    ax.text((x0 + X_OUT) / 2 - 0.2, Y_KEEP / 2 + 0.45, "p", ha="center", va="center", fontsize=15, color=BLACK)
    ax.text((x0 + X_OUT) / 2 - 0.45, Y_DROP / 2 - 0.4, "1−p", ha="center", va="center", fontsize=15, color=BLACK)
    node(ax, X_OUT, Y_KEEP, "a")
    node(ax, X_OUT, Y_DROP, "0", ls="--")
    ax.text(X_OUT + R + 0.15, Y_KEEP, "그대로", ha="left", va="center", fontsize=13, color=BLACK)
    ax.text(X_OUT + R + 0.15, Y_DROP, "꺼짐", ha="left", va="center", fontsize=13, color=BLACK)

    for x, label in ((X_IN, "입력"), (X_SUM, "가중합"), (X_ACT, "활성화 함수")):
        ax.text(x, 2.45, label, ha="center", va="center", fontsize=15, color=BLACK)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
