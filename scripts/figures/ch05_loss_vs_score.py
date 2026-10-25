"""정답이 1일 때 점수 z에 따른 MSE와 BCE 손실을 비교하는 PNG를 만든다.

실행: python3 scripts/figures/ch05_loss_vs_score.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font, sigmoid


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch04/loss-vs-score.png"
MSE_COLOR = "#e6772e"
BCE_COLOR = "#315f7d"


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.1, right=0.97, bottom=0.17, top=0.94)
    z = np.linspace(-7, 3, 1000)
    p = sigmoid(z)
    ax.plot(z, (1 - p) ** 2, color=MSE_COLOR, linewidth=2.8)
    ax.plot(z, np.log1p(np.exp(-z)), color=BCE_COLOR, linewidth=2.8)

    ax.text(-6.9, 1.3, "MSE", fontsize=15, color=MSE_COLOR, fontweight="bold")
    ax.text(-4.6, 5.2, "BCE", fontsize=15, color=BCE_COLOR, fontweight="bold")

    ax.set(xlim=(-7.2, 3.2), ylim=(-0.2, 7.2),
           xticks=[-6, -4, -2, 0, 2], yticks=[0, 1, 2, 4, 6],
           xlabel="점수 z (정답 y = 1)", ylabel="손실")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#777777")
    ax.grid(color="#e8ebee", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=12, colors="#444444")
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
