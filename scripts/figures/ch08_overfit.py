"""훈련 데이터에 딱 맞춘 깊은 모델이 새 데이터 하나에서 크게 틀리는 과적합 PNG를 만든다.

점은 sin 곡선에 잡음을 얹은 훈련 데이터 9개와, 훈련 범위 오른쪽 밖에서 같은 곡선 위에 놓인
새 데이터 1개다. 깊은 신경망은 훈련 점을 모두 지나는 8차 다항식으로 흉내 낸다. 훈련 오차는 0이지만
마지막 훈련 점을 지나자 곡선이 꺾여 새 데이터와 멀리 떨어진다.
비교용 단순한 모델(초록)은 3차 다항식이라 큰 흐름만 따라가고, 새 데이터 근처를 지난다.

실행: python3 scripts/figures/ch08_overfit.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch07/overfit.png"
CURVE = "#315f7d"
ORANGE = "#e87924"
RED = "#dc2626"
DARK = "#334155"
GREEN = "#2f9e44"


def truth(x):
    return 1.6 + 1.2 * np.sin(2 * np.pi * x)


rng = np.random.default_rng(14)
X_TRAIN = np.linspace(0.05, 0.9, 9)
Y_TRAIN = truth(X_TRAIN) + rng.normal(0, 0.25, X_TRAIN.size)
X_NEW = 0.985
Y_NEW = truth(X_NEW)


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.06, top=0.96)

    coef = np.polyfit(X_TRAIN, Y_TRAIN, X_TRAIN.size - 1)
    xs = np.linspace(X_TRAIN[0], 1.06, 400)
    pred = np.polyval(coef, X_NEW)
    simple = np.polyfit(X_TRAIN, Y_TRAIN, 3)

    ax.vlines(X_NEW, pred, Y_NEW, color=RED, lw=2.0, zorder=2)
    ax.plot(xs, np.polyval(simple, xs), color=GREEN, lw=3.2, zorder=3)
    ax.plot(xs, np.polyval(coef, xs), color=ORANGE, lw=3.2, zorder=3)
    ax.scatter(X_TRAIN, Y_TRAIN, color=CURVE, s=48, zorder=4)
    ax.scatter([X_NEW], [Y_NEW], facecolor="white", edgecolor=DARK, lw=1.8, s=70, zorder=4)

    box = dict(fc="white", ec="none", pad=1.5)
    ax.text(0.06, 1.15, "과적합 모델", ha="left", va="center",
            fontsize=14, color=ORANGE, fontweight="bold", zorder=5)
    ax.text(0.46, 2.5, "단순한 모델", ha="left", va="center",
            fontsize=14, color=GREEN, fontweight="bold", zorder=5)
    ax.text(X_TRAIN[6], Y_TRAIN[6] - 0.4, "훈련 데이터", ha="center", va="top",
            fontsize=14, color=CURVE, fontweight="bold", zorder=5)
    ax.text(X_NEW - 0.025, Y_NEW + 0.12, "새 데이터", ha="right", va="bottom",
            fontsize=14, color=DARK, fontweight="bold", bbox=box, zorder=5)
    ax.text(X_NEW + 0.012, (Y_NEW + pred) / 2, "오차", ha="left", va="center",
            fontsize=13, color=RED, zorder=5)

    ax.set(xlim=(0, 1.06), ylim=(-0.8, 3.2), xticks=[], yticks=[])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#777777")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
