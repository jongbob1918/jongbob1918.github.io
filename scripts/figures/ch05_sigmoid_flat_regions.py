"""시그모이드의 양쪽 포화 구간을 빨간 타원으로 표시한 PNG를 만든다.

실행: python3 scripts/figures/ch05_sigmoid_flat_regions.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

from ch05_sigmoid_animation import set_korean_font, sigmoid


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch04/sigmoid-flat-regions.png"


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.17, top=0.94)
    z = np.linspace(-7, 7, 1000)
    ax.plot(z, sigmoid(z), color="#315f7d", linewidth=2.8)
    # The outlined intervals are illustrative, not a sharp saturation cutoff.
    for center in (-5.25, 5.25):
        ax.add_patch(Ellipse((center, sigmoid(center)), width=3.35, height=0.16,
                             facecolor="none", edgecolor="#d63b35", linewidth=2))
    ax.set(xlim=(-7.25, 7.25), ylim=(-0.13, 1.13),
           xticks=[-6, -3, 0, 3, 6], yticks=[0, 0.5, 1],
           xlabel="점수 z", ylabel="출력 p")
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
