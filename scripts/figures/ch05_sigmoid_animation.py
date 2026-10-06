"""시그모이드에서 입력 z가 커질 때 분모와 출력이 변하는 GIF를 만든다.

실행: python3 scripts/figures/ch05_sigmoid_animation.py
출력: site/public/images/notes/easy-deep-learning-ch04/sigmoid-input.gif
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.animation import FuncAnimation, PillowWriter


OUT = (
    Path(__file__).resolve().parents[2]
    / "site/public/images/notes/easy-deep-learning-ch04/sigmoid-input.gif"
)
BLUE = "#315f7d"
ORANGE = "#e6772e"
GRAY = "#d7dce0"
DARK = "#292929"


def set_korean_font():
    candidates = (
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "C:/Windows/Fonts/malgun.ttf",
    )
    for path in candidates:
        if Path(path).exists():
            font_manager.fontManager.addfont(path)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
            return


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def main():
    set_korean_font()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(7, 5), dpi=100, facecolor="white")
    grid = fig.add_gridspec(2, 1, height_ratios=(3.3, 1.2), hspace=0.06)
    ax = fig.add_subplot(grid[0])
    formula_ax = fig.add_subplot(grid[1])

    curve_z = np.linspace(-6, 6, 800)
    curve_y = sigmoid(curve_z)
    ax.plot(curve_z, curve_y, color=BLUE, linewidth=2.6)
    trail, = ax.plot([], [], color=ORANGE, linewidth=3.2)
    point, = ax.plot([], [], "o", color=ORANGE, markersize=10, zorder=4)
    vertical, = ax.plot([], [], color=ORANGE, linewidth=1.2, linestyle="--", alpha=0.45)
    horizontal, = ax.plot([], [], color=ORANGE, linewidth=1.2, linestyle="--", alpha=0.45)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-0.04, 1.04)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("입력", fontsize=15, color=DARK, labelpad=8)
    ax.set_ylabel("출력", fontsize=15, color=DARK, labelpad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(DARK)
    ax.spines[["left", "bottom"]].set_linewidth(1.5)

    formula_ax.axis("off")
    input_text = formula_ax.text(
        0.5, 0.72, "", ha="center", va="center", fontsize=16, color=DARK
    )
    formula_text = formula_ax.text(
        0.5, 0.26, "", ha="center", va="center", fontsize=17, color=DARK
    )

    moving = np.linspace(0, 5, 61)
    frames = np.concatenate((np.repeat(moving[0], 8), moving, np.repeat(moving[-1], 16)))

    def update(z):
        output = float(sigmoid(z))
        denominator = 1 + np.exp(-z)
        exponent = 0.0 if abs(z) < 0.05 else -z
        shown_z = 0.0 if abs(z) < 0.05 else z

        trail_z = np.linspace(0, z, max(2, int(z * 30) + 2))
        trail.set_data(trail_z, sigmoid(trail_z))
        point.set_data([z], [output])
        vertical.set_data([z, z], [0, output])
        horizontal.set_data([-6, z], [output, output])

        input_text.set_text(f"입력  z = {shown_z:.1f}")
        formula_text.set_text(
            rf"$\sigma({shown_z:.1f})="
            rf"\dfrac{{1}}{{1+e^{{{exponent:.1f}}}}}="
            rf"\dfrac{{1}}{{{denominator:.3f}}}={output:.3f}$"
        )
        return trail, point, vertical, horizontal, input_text, formula_text

    animation = FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=lambda: update(frames[0]),
        interval=1000 / 15,
        blit=True,
    )
    fig.subplots_adjust(left=0.12, right=0.97, top=0.97, bottom=0.05)
    animation.save(OUT, writer=PillowWriter(fps=15), dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    main()
