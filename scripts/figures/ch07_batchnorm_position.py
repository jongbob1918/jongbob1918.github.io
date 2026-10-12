"""인공신경망 은닉 노드마다 가중합과 활성화 함수 사이에 배치 정규화 모듈이 들어가는 PNG를 만든다.

실행: python3 scripts/figures/ch07_batchnorm_position.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06/batchnorm-position.png"
CURVE = "#315f7d"
ORANGE = "#e87924"
DARK = "#334155"
GRAY = "#94a3b8"
R = 0.42
BN_W, BN_H = 2.0, 0.9

X_IN, X_SUM, X_BN, X_ACT, X_OUT = 0.0, 3.2, 5.3, 7.4, 10.6
INPUTS = [1.0, -1.0]
HIDDEN = [2.0, 0.0, -2.0]
OUTPUTS = [1.0, -1.0]


def node(ax, x, y, text, edge=CURVE, size=17):
    ax.add_patch(Circle((x, y), R, fc="white", ec=edge, lw=2.4, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=size, color=edge, zorder=4)


def line(ax, p, q):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.3, zorder=1)


def arrow(ax, x0, x1, y, color=GRAY):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=15,
                                 color=color, lw=1.8, shrinkA=0, shrinkB=0, zorder=2))


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(9.4, 4.8), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
    ax.set_aspect("equal")
    ax.set(xlim=(-0.9, 11.5), ylim=(-3.3, 4.3))
    ax.axis("off")

    for y_in in INPUTS:
        for y_h in HIDDEN:
            line(ax, (X_IN + R, y_in), (X_SUM - R, y_h))
    for y_h in HIDDEN:
        for y_o in OUTPUTS:
            line(ax, (X_ACT + R, y_h), (X_OUT - R, y_o))

    for i, y in enumerate(INPUTS, start=1):
        node(ax, X_IN, y, f"$x_{i}$")
    for y in HIDDEN:
        node(ax, X_SUM, y, "Σ")
        # 배치 정규화는 노드마다 따로 적용한다: 노드 하나의 가중합을 배치 전체에 걸쳐 정규화
        ax.add_patch(FancyBboxPatch((X_BN - BN_W / 2, y - BN_H / 2), BN_W, BN_H,
                                    boxstyle="round,pad=0.02,rounding_size=0.25",
                                    fc="#fff4e8", ec=ORANGE, lw=2.4, zorder=2))
        ax.text(X_BN, y, "배치 정규화", ha="center", va="center",
                fontsize=14, fontweight="bold", color=ORANGE, zorder=4)
        arrow(ax, X_SUM + R, X_BN - BN_W / 2 - 0.02, y)
        arrow(ax, X_BN + BN_W / 2 + 0.02, X_ACT - R, y)
        node(ax, X_ACT, y, "f")
    for i, y in enumerate(OUTPUTS, start=1):
        node(ax, X_OUT, y, f"$y_{i}$")

    for x, label in ((X_IN, "입력"), (X_SUM, "가중합"), (X_ACT, "활성화 함수"), (X_OUT, "출력")):
        ax.text(x, 3.55, label, ha="center", va="center", fontsize=15, color=DARK)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
