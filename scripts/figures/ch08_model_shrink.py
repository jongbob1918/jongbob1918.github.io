"""층과 노드를 줄여 모델을 가볍게 만들면 학습된 곡선이 단순해지는 PNG를 만든다.

왼쪽은 입력 1개, 은닉층 3개(노드 5개씩), 출력 1개인 신경망이고 오른쪽은 은닉층 1개(노드 3개)만 남긴 신경망이다.
아래 곡선은 과적합 그림(ch08_overfit.py)과 같은 훈련 데이터에 맞춘 8차·3차 다항식으로 두 모델을 흉내 낸다.

실행: python3 scripts/figures/ch08_model_shrink.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

from ch05_sigmoid_animation import set_korean_font
from ch08_overfit import CURVE, X_TRAIN, Y_TRAIN


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch07/model-shrink.png"
BLACK = "#222222"
GRAY = "#94a3b8"
R = 0.3
GAP = 1.6

BIG = (1, 5, 5, 5, 1)
SMALL = (1, 3, 1)


def network(ax, layers, color):
    width = GAP * (len(layers) - 1)
    x0 = (GAP * (len(BIG) - 1) - width) / 2
    pos = [[(x0 + i * GAP, y) for y in np.arange(n)[::-1] - (n - 1) / 2] for i, n in enumerate(layers)]
    for left, right in zip(pos, pos[1:]):
        for p in left:
            for q in right:
                ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.0, zorder=1)
    for layer in pos:
        for x, y in layer:
            ax.add_patch(Circle((x, y), R, fc="white", ec=color, lw=2.2, zorder=2))
    ax.set_aspect("equal")
    ax.set(xlim=(-0.6, GAP * (len(BIG) - 1) + 0.6), ylim=(-2.4, 2.4))
    ax.axis("off")
    return sum(a * b for a, b in zip(layers, layers[1:]))


def curve(ax, degree, color):
    coef = np.polyfit(X_TRAIN, Y_TRAIN, degree)
    xs = np.linspace(X_TRAIN[0], 1.0, 400)
    ax.plot(xs, np.polyval(coef, xs), color=color, lw=3.0, zorder=2)
    ax.scatter(X_TRAIN, Y_TRAIN, color=CURVE, s=34, zorder=3)
    ax.set(xlim=(0, 1.0), ylim=(-0.8, 3.2), xticks=[], yticks=[])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#777777")


def render():
    set_korean_font()
    fig = plt.figure(figsize=(10.0, 5.0), dpi=200, facecolor="white")
    grid = fig.add_gridspec(2, 3, width_ratios=(1, 0.32, 1), height_ratios=(1.15, 0.85),
                            left=0.03, right=0.97, bottom=0.04, top=0.86, wspace=0.05, hspace=0.08)

    for col, layers, degree, color, title in ((0, BIG, 8, BLACK, "깊고 넓은 신경망"),
                                              (2, SMALL, 3, BLACK, "가벼운 신경망")):
        weights = network(fig.add_subplot(grid[0, col]), layers, color)
        curve(fig.add_subplot(grid[1, col]), degree, color)
        center = grid[0, col].get_position(fig)
        x = (center.x0 + center.x1) / 2
        fig.text(x, 0.955, title, ha="center", va="center", fontsize=16, fontweight="bold", color=color)
        fig.text(x, 0.895, f"가중치 {weights}개", ha="center", va="center", fontsize=13, color=BLACK)

    mid = grid[0, 1].get_position(fig)
    y = (mid.y0 + mid.y1) / 2
    fig.patches.append(FancyArrowPatch((mid.x0 + 0.005, y), (mid.x1 - 0.005, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=20, color=BLACK, lw=2.0))
    fig.text((mid.x0 + mid.x1) / 2, y + 0.045, "층·노드 줄이기", ha="center", va="center",
             fontsize=13, color=BLACK)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
