"""일반 신경망과 드롭아웃으로 일부 노드를 끈 신경망을 나란히 비교하는 PNG를 만든다.

Srivastava et al.(2014) Figure 1처럼 꺼진 노드에 X를 긋고, 그 노드에 연결된 선을 지운다.

실행: python3 scripts/figures/ch08_dropout_network.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch07/dropout-network.png"
BLACK = "#222222"
GRAY = "#94a3b8"
LIGHT = "#bbbbbb"
R = 0.3
GAP = 1.8

LAYERS = (4, 5, 5, 2)
# (층 번호, 위에서부터 노드 번호): 은닉층에서만 끈다
DROPPED = {(1, 1), (1, 3), (2, 0), (2, 2), (2, 4)}


def network(ax, dropped):
    pos = [[(i * GAP, y) for y in np.arange(n)[::-1] - (n - 1) / 2] for i, n in enumerate(LAYERS)]
    for i, (left, right) in enumerate(zip(pos, pos[1:])):
        for a, p in enumerate(left):
            for b, q in enumerate(right):
                if (i, a) in dropped or (i + 1, b) in dropped:
                    continue
                ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.0, zorder=1)
    for i, layer in enumerate(pos):
        for j, (x, y) in enumerate(layer):
            if (i, j) in dropped:
                ax.add_patch(Circle((x, y), R, fc="white", ec=LIGHT, lw=2.0, ls="--", zorder=2))
                d = R * 0.75
                ax.plot([x - d, x + d], [y - d, y + d], color=BLACK, lw=2.4, zorder=3)
                ax.plot([x - d, x + d], [y + d, y - d], color=BLACK, lw=2.4, zorder=3)
            else:
                ax.add_patch(Circle((x, y), R, fc="white", ec=BLACK, lw=2.2, zorder=2))
    ax.set_aspect("equal")
    ax.set(xlim=(-0.6, GAP * (len(LAYERS) - 1) + 0.6), ylim=(-2.45, 2.45))
    ax.axis("off")


def render():
    set_korean_font()
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.8), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.03, right=0.97, bottom=0.02, top=0.9, wspace=0.25)
    for ax, dropped, title in ((axes[0], set(), "일반 신경망"), (axes[1], DROPPED, "드롭아웃 적용")):
        network(ax, dropped)
        ax.set_title(title, fontsize=16, fontweight="bold", color=BLACK, pad=10)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
