"""학생 8명의 데이터와 유닛 스텝·시그모이드 분류 경계를 그린다.

실행: python3 scripts/figures/ch05_linear_classification.py
동일한 점수 z = x1 + x2 / 10 - 10에서 unit step의 기준은 z=0,
sigmoid의 기준은 p=0.5이다. 두 경계는 같은 직선이다.
출력: perceptron-data.png, perceptron-boundary.png,
      unit-step-sigmoid-boundary.png (easy-deep-learning-ch04 폴더)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D

from ch04_classification_drawio import PASS, FAIL, perceptron, OUT as DIAGRAMS


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch04"
PASS_COLOR, FAIL_COLOR = "#315a7a", "#e07b39"
STEP_COLOR, SIGMOID_COLOR = "#8b5bb5", "#258978"


def configure_font():
    for candidate in (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
    ):
        if Path(candidate).exists():
            font_manager.fontManager.addfont(candidate)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=candidate).get_name()
            break
    plt.rcParams.update({"font.size": 14, "axes.unicode_minus": False})


def draw_data(ax):
    for samples, marker, color in (
        (PASS, "o", PASS_COLOR), (FAIL, "D", FAIL_COLOR)
    ):
        values = np.asarray(samples)
        ax.scatter(values[:, 0], values[:, 1], s=95, marker=marker,
                   color=color, edgecolors="white", linewidths=1, zorder=3)
    ax.set(xlim=(0, 10), ylim=(0, 100), xticks=[0, 2, 4, 6, 8, 10],
           yticks=[0, 20, 40, 60, 80, 100],
           xlabel="공부 시간 (시간)", ylabel="출석률 (%)")
    ax.grid(color="#e4e7ea", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#757575")
    ax.tick_params(colors="#444444", labelsize=12)


def draw_boundary(ax, color):
    x = np.linspace(0, 10, 101)
    ax.plot(x, 100 - 10 * x, color=color, linewidth=2.8, zorder=2)


def save_single(name, boundary=False):
    fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=200)
    fig.subplots_adjust(left=0.14, right=0.97, bottom=0.18, top=0.84)
    draw_data(ax)
    if boundary:
        draw_boundary(ax, STEP_COLOR)
        fig.legend([Line2D([0], [0], color=STEP_COLOR, linewidth=2.8)],
                   ["유닛 스텝"], loc="upper center", frameon=False,
                   bbox_to_anchor=(0.55, 0.99))
    fig.savefig(OUT / f"{name}.png", facecolor="white")
    plt.close(fig)


def save_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), dpi=200)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.83, wspace=0.28)
    for ax, color in zip(axes, (STEP_COLOR, SIGMOID_COLOR)):
        draw_data(ax)
        draw_boundary(ax, color)
    fig.legend([Line2D([0], [0], color=color, linewidth=2.8)
                for color in (STEP_COLOR, SIGMOID_COLOR)],
               ["유닛 스텝", "시그모이드"], ncol=2, loc="upper center",
               frameon=False, bbox_to_anchor=(0.53, 0.99))
    fig.savefig(OUT / "unit-step-sigmoid-boundary.png", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    configure_font()
    OUT.mkdir(parents=True, exist_ok=True)
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    # Keep the existing editable draw.io originals on the same eight students.
    perceptron(False)
    perceptron(True)
    save_single("perceptron-data")
    save_single("perceptron-boundary", boundary=True)
    save_comparison()
