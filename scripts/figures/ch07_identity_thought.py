"""ResNet 논문의 사고 실험(20층 + 항등 층 36개)과 실제 56층 학습 결과를 층 블록으로 비교한 PNG를 만든다.

20층을 그대로 복사하고 항등 층 36개를 덧붙인 56층은 20층과 같은 출력을 낸다.
같은 56층이라도 처음부터 학습하면 훈련 오차가 20층보다 높았다.

실행: python3 scripts/figures/ch07_identity_thought.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

from ch05_sigmoid_animation import set_korean_font

OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06/identity-thought-experiment.png"
CURVE = "#315f7d"
ORANGE = "#e87924"
DARK = "#334155"
GRAY = "#94a3b8"
RED = "#dc2626"

X0 = 3.0          # 첫 블록의 왼쪽 x
PITCH = 0.22      # 블록 간격
BW, BH = 0.16, 0.9
ROWS = {"base": 3.2, "thought": 1.2, "real": -1.3}
X_END = X0 + 56 * PITCH
X_ERR = X_END + 1.6


def block(ax, i, y, style):
    x = X0 + i * PITCH
    if style == "learned":
        ax.add_patch(Rectangle((x, y - BH / 2), BW, BH, fc="#dbe7f0", ec=CURVE, lw=1.2))
    elif style == "identity":
        ax.add_patch(Rectangle((x, y - BH / 2), BW, BH, fc="white", ec=GRAY, lw=1.0, ls=(0, (2, 1.5))))
    else:
        ax.add_patch(Rectangle((x, y - BH / 2), BW, BH, fc="#fff4e8", ec=ORANGE, lw=1.2))


def arrow(ax, x0, x1, y0, y1, color=GRAY, lw=1.6, ls="-"):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0))


def row_label(ax, y, title, sub=None):
    ax.text(X0 - 0.35, y + (0.17 if sub else 0), title, ha="right", va="center", fontsize=15,
            fontweight="bold", color=DARK)
    if sub:
        ax.text(X0 - 0.35, y - 0.3, sub, ha="right", va="center", fontsize=12, color=GRAY)


def result(ax, y, last_x, text, color, bold=False):
    arrow(ax, last_x + 0.25, X_ERR - 0.95, y, y)
    ax.text(X_ERR, y, text, ha="center", va="center", fontsize=15, color=color,
            fontweight="bold" if bold else "normal")


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(12.0, 4.6), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
    ax.set_aspect("equal")
    ax.set(xlim=(0.8, X_ERR + 1.0), ylim=(-2.0, 4.7))
    ax.axis("off")

    ax.text(X_ERR, 4.35, "훈련 오차", ha="center", va="center", fontsize=13, color=GRAY)

    # 20층
    y = ROWS["base"]
    row_label(ax, y, "20층")
    for i in range(20):
        block(ax, i, y, "learned")
    result(ax, y, X0 + 19 * PITCH + BW, "기준", DARK)

    # 사고 실험: 20층 복사 + 항등 층 36개
    y = ROWS["thought"]
    row_label(ax, y, "56층", "사고 실험")
    for i in range(20):
        block(ax, i, y, "learned")
    for i in range(20, 56):
        block(ax, i, y, "identity")
    mid = X0 + 10 * PITCH
    arrow(ax, mid, mid, ROWS["base"] - BH / 2 - 0.08, y + BH / 2 + 0.08, color=CURVE, lw=1.4, ls=(0, (3, 2)))
    ax.text(mid + 0.18, (ROWS["base"] + y) / 2, "복사", ha="left", va="center", fontsize=12, color=CURVE)
    gx0, gx1 = X0 + 20 * PITCH, X0 + 55 * PITCH + BW
    ax.plot([gx0, gx0, gx1, gx1], [y + BH / 2 + 0.12, y + BH / 2 + 0.22, y + BH / 2 + 0.22, y + BH / 2 + 0.12],
            color=GRAY, lw=1.2)
    ax.text((gx0 + gx1) / 2, y + BH / 2 + 0.45, "y = x  ×36", ha="center", va="center", fontsize=13, color=GRAY)
    result(ax, y, X_END, "= 20층", CURVE, bold=True)

    # 실제 학습
    y = ROWS["real"]
    ax.plot([X0 - 2.6, X_ERR + 0.9], [(ROWS["thought"] + y) / 2 - 0.05] * 2, color="#e2e8f0", lw=1.2)
    row_label(ax, y, "56층", "처음부터 학습")
    for i in range(56):
        block(ax, i, y, "trained")
    result(ax, y, X_END, "> 20층", RED, bold=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
