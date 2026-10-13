"""학습을 오래 할수록 훈련 오차는 계속 줄지만 검증 오차는 어느 순간부터 다시 커지는 PNG를 만든다.

두 곡선은 실제 학습 기록이 아니라 모양을 보여주기 위한 식이다.
검증 오차가 가장 작은 에포크에 세로선을 긋고 그 시점에서 학습을 멈춘다고 표시한다.

실행: python3 scripts/figures/ch08_early_stopping.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch07/early-stopping.png"
BLACK = "#222222"
GRAY = "#94a3b8"

EPOCH = np.linspace(0, 60, 400)
TRAIN = 0.1 + 1.7 * np.exp(-EPOCH / 10)
VALID = 0.3 + 1.7 * np.exp(-EPOCH / 10) + 0.0004 * EPOCH ** 2


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.08, right=0.97, bottom=0.1, top=0.96)

    best = int(np.argmin(VALID))
    stop = EPOCH[best]
    ax.axvspan(stop, EPOCH[-1], color="#f1f5f9", zorder=0)
    ax.axvline(stop, color=GRAY, lw=1.6, ls=(0, (4, 3)), zorder=1)

    ax.plot(EPOCH, TRAIN, color=BLACK, lw=2.8, zorder=2)
    ax.plot(EPOCH, VALID, color=BLACK, lw=2.8, ls=(0, (5, 3)), zorder=2)
    ax.scatter([stop], [VALID[best]], color=BLACK, s=60, zorder=3)

    ax.text(EPOCH[-1] - 1, TRAIN[-1] + 0.1, "훈련 데이터 오차", ha="right", va="bottom",
            fontsize=13, color=BLACK)
    ax.text(EPOCH[-1] - 1, VALID[-1] + 0.1, "검증 데이터 오차", ha="right", va="bottom",
            fontsize=13, color=BLACK)
    ax.text(stop + 1, VALID[best] + 0.08, "학습 중단", ha="left", va="bottom",
            fontsize=14, fontweight="bold", color=BLACK)
    ax.text((stop + EPOCH[-1]) / 2, 0.55, "과적합 구간", ha="center", va="center",
            fontsize=14, color="#64748b")

    ax.set(xlim=(0, 60), ylim=(0, 2.1), xticks=[], yticks=[])
    ax.set_xlabel("학습 횟수(에포크)", fontsize=13, color=BLACK)
    ax.set_ylabel("오차", fontsize=13, color=BLACK)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#777777")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
