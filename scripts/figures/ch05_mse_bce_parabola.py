"""정답이 1일 때 예측 p에 따른 MSE(포물선)와 BCE를 비교하는 PNG를 만든다.

실행: python3 scripts/figures/ch05_mse_bce_parabola.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch04/mse-bce-parabola.png"
MSE_COLOR = "#e6772e"
BCE_COLOR = "#315f7d"
DASH = (0, (5, 3))


def render():
    set_korean_font()
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.1, right=0.97, bottom=0.17, top=0.94)

    # 확률 p가 있을 수 있는 0~1 구간만 진하게, 바깥은 포물선 모양을 보여 주려고 흐리게 그린다.
    ax.axvspan(0, 1, color="#f1f3f5", zorder=0)
    ax.text(0.5, 4.85, "확률 p의 범위", ha="center", fontsize=12, color="#666666")
    outside = np.linspace(-1.2, 3.2, 600)
    ax.plot(outside, (outside - 1) ** 2, color=MSE_COLOR, alpha=0.35, linewidth=2, linestyle=DASH)
    p = np.linspace(0, 1, 300)
    ax.plot(p, (p - 1) ** 2, color=MSE_COLOR, linewidth=2.8)
    p = np.linspace(np.exp(-5.2), 1, 600)
    ax.plot(p, -np.log(p), color=BCE_COLOR, linewidth=2.8)

    ax.text(1.75, 1.75, "MSE", fontsize=15, color=MSE_COLOR, fontweight="bold")
    ax.text(0.2, 2.6, "BCE", fontsize=15, color=BCE_COLOR, fontweight="bold")

    ax.set(xlim=(-1.2, 3.2), ylim=(-0.2, 5.2),
           xticks=[-1, 0, 1, 2, 3], yticks=[0, 1, 2, 3, 4, 5],
           xlabel="예측 p (정답 y = 1)", ylabel="손실")
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
