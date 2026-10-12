"""큰 흐름은 따라가지만 잔물결 같은 미세한 패턴을 놓치는 과소적합 PNG를 만든다.

점(X, Y)은 큰 곡선 위에 작은 물결이 얹힌 데이터다. 모델은 3차 다항식 하나라서 부드러운
큰 흐름만 따라가고, 점과 선 사이 작은 오차가 물결 모양으로 남는다.
점은 7절 과적합 그림에서도 같이 쓸 수 있게 상수로 둔다.

실행: python3 scripts/figures/ch07_underfit.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06/underfit.png"
CURVE = "#315f7d"
ORANGE = "#e87924"
RED = "#dc2626"
GRAY = "#94a3b8"

X = np.linspace(0.03, 0.97, 24)
Y = (0.6 + 2.4 * np.sin(np.pi * X) + 0.36 * np.sin(2 * np.pi * 3 * X)
     + np.random.default_rng(7).normal(0, 0.04, X.size))


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.06, top=0.96)

    coef = np.polyfit(X, Y, 3)
    pred = np.polyval(coef, X)
    xs = np.linspace(X[0] - 0.02, X[-1] + 0.02, 300)

    ax.vlines(X, pred, Y, color=RED, lw=1.6, alpha=0.75, zorder=2)
    ax.plot(xs, np.polyval(coef, xs), color=ORANGE, lw=3.2, zorder=3)
    ax.scatter(X, Y, color=CURVE, s=48, zorder=4)

    box = dict(fc="white", ec="none", pad=1.5)
    ax.text(0.04, 0.55, "모델(부드러운 곡선)", ha="left", va="center",
            fontsize=14, color=ORANGE, fontweight="bold", zorder=5)
    top = int(np.argmax(Y))
    ax.text(X[top], Y[top] + 0.17, "데이터", ha="center", va="bottom",
            fontsize=14, color=CURVE, fontweight="bold", zorder=5)
    below = np.where(Y < pred, pred - Y, 0)
    gap = int(np.argmax(below))
    ax.text(X[gap], Y[gap] - 0.2, "남는 오차", ha="center", va="top",
            fontsize=13, color=RED, bbox=box, zorder=5)

    ax.set(xlim=(0, 1), ylim=(0, 3.9), xticks=[], yticks=[])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#777777")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
