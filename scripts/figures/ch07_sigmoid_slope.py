"""시그모이드의 x=0 접선(기울기 0.25)을 표시한 PNG를 만든다.

실행: python3 scripts/figures/ch07_sigmoid_slope.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font, sigmoid


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06/sigmoid-max-slope.png"
CURVE = "#315f7d"
ORANGE = "#e87924"
GRAY = "#94a3b8"


def tangent(ax, x0, half_width, **style):
    y0 = sigmoid(x0)
    slope = y0 * (1 - y0)
    x = np.array([x0 - half_width, x0 + half_width])
    ax.plot(x, y0 + slope * (x - x0), **style)
    return y0, slope


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.17, top=0.94)

    z = np.linspace(-7, 7, 1000)
    ax.plot(z, sigmoid(z), color=CURVE, linewidth=2.8, zorder=3)

    # 비교용: 0에서 멀어지면 같은 길이의 접선이 더 눕는다.
    for x0 in (-3, 3):
        y0, slope = tangent(ax, x0, 1.2, color=GRAY, linewidth=2, linestyle="--", zorder=2)
        ax.scatter([x0], [y0], color=GRAY, s=36, zorder=4)
        ax.annotate(f"기울기 {slope:.2f}", (x0, y0), xytext=(0, 20 if x0 < 0 else -28),
                    textcoords="offset points", ha="center", fontsize=12, color="#64748b")

    y0, slope = tangent(ax, 0, 1.4, color=ORANGE, linewidth=3, zorder=5)
    ax.scatter([0], [y0], color=ORANGE, s=60, zorder=6)
    ax.annotate(f"x=0에서 기울기 {slope:.2f} (최대)\n출력 f(0)=0.5", (0, y0),
                xytext=(-150, 48), textcoords="offset points", ha="center",
                fontsize=13, color=ORANGE, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=ORANGE, linewidth=1.2))

    ax.set(xlim=(-7.25, 7.25), ylim=(-0.08, 1.08),
           xticks=[-6, -3, 0, 3, 6], yticks=[0, 0.5, 1],
           xlabel="입력 x", ylabel="출력 f(x)")
    ax.set_yticklabels(["0", "0.5", "1"])
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
