"""ReLU 기본 그래프 PNG를 만든다.

실행: python3 scripts/figures/ch07_relu.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06/relu.png"
CURVE = "#315f7d"
ORANGE = "#e87924"


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.17, top=0.94)

    x = np.linspace(-4, 4, 801)
    ax.plot(x, np.maximum(0, x), color=CURVE, linewidth=3.2, zorder=3)
    ax.scatter([0], [0], color=ORANGE, s=60, zorder=4)

    ax.annotate("음수는 0으로 출력", (-2, 0), xytext=(0, 16), textcoords="offset points",
                ha="center", fontsize=13, color=ORANGE, fontweight="bold")
    ax.annotate("양수는 그대로 출력", (2.4, 2.4), xytext=(-12, 8), textcoords="offset points",
                ha="right", fontsize=13, color=ORANGE, fontweight="bold")

    ax.set(xlim=(-4.2, 4.2), ylim=(-0.4, 4.3),
           xticks=[-4, -2, 0, 2, 4], yticks=[0, 2, 4],
           xlabel="입력 x", ylabel="출력 f(x)")
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
