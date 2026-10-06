"""라벨 오류 하나로 퍼셉트론 경계가 수렴하지 않는 GIF를 만든다.

실행: python3 scripts/figures/ch05_perceptron_nonconvergence.py
출력: site/public/images/notes/easy-deep-learning-ch04/perceptron-nonconvergence.gif
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
    / "site/public/images/notes/easy-deep-learning-ch04/perceptron-nonconvergence.gif"
)
BLUE = "#315f7d"
ORANGE = "#e6772e"
RED = "#c8453c"
DARK = "#292929"

PASS = np.array(
    [
        (3.5, 85),
        (4.5, 75),
        (5, 65),
        (6, 60),
        (6.5, 85),
        (7, 50),
        (7.5, 40),
        (8, 70),
        (9, 60),
        (9.2, 30),
    ],
    dtype=float,
)
FAIL = np.array(
    [
        (1, 40),
        (1, 80),
        (1.5, 65),
        (2, 30),
        (2.5, 55),
        (3, 20),
        (4, 35),
        (5, 30),
        (6, 20),
        (7, 10),
    ],
    dtype=float,
)
WRONG_LABEL = np.array((6, 60), dtype=float)


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


def training_updates(count=32):
    pass_points = np.array([p for p in PASS if not np.allclose(p, WRONG_LABEL)])
    fail_points = np.vstack((FAIL, WRONG_LABEL))
    raw_x = np.vstack((fail_points, pass_points))
    x = raw_x / np.array((10, 100))
    y = np.concatenate((-np.ones(len(fail_points)), np.ones(len(pass_points))))

    weights = np.array((1.0, 1.0))
    bias = -1.0
    updates = []

    while len(updates) < count:
        for raw_point, point, label in zip(raw_x, x, y):
            if label * (weights @ point + bias) <= 0:
                weights = weights + 0.2 * label * point
                bias = bias + 0.2 * label
                updates.append((weights.copy(), bias, raw_point.copy()))
                if len(updates) == count:
                    break

    return pass_points, fail_points, updates


def boundary_segment(weights, bias):
    x = np.array((0.0, 10.0))
    normalized_x = x / 10
    y = -(weights[0] * normalized_x + bias) / weights[1] * 100
    return x, y


def main():
    set_korean_font()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pass_points, fail_points, updates = training_updates()

    fig, ax = plt.subplots(figsize=(7, 4.6), dpi=100, facecolor="white")
    ax.scatter(
        pass_points[:, 0], pass_points[:, 1], s=90, marker="o", color=BLUE, zorder=3
    )
    ax.scatter(
        fail_points[:, 0], fail_points[:, 1], s=100, marker="D", color=ORANGE, zorder=3
    )
    boundary, = ax.plot([], [], color=RED, linewidth=3.2, zorder=2)
    active = ax.scatter(
        [], [], s=220, facecolors="none", edgecolors=DARK, linewidths=2.0, zorder=4
    )

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 100)
    ax.set_xticks(np.arange(0, 11, 2))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    ax.grid(color="#d9dde0", linewidth=1.0)
    ax.set_axisbelow(True)
    ax.set_xlabel("공부 시간", fontsize=15, color=DARK, labelpad=9)
    ax.set_ylabel("출석률", fontsize=15, color=DARK, labelpad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(DARK)
    ax.spines[["left", "bottom"]].set_linewidth(1.5)

    def update(frame):
        weights, bias, point = updates[frame]
        x, y = boundary_segment(weights, bias)
        boundary.set_data(x, y)
        active.set_offsets(point.reshape(1, 2))
        return boundary, active

    animation = FuncAnimation(
        fig,
        update,
        frames=len(updates),
        init_func=lambda: update(0),
        interval=180,
        blit=True,
    )
    fig.tight_layout(pad=1.2)
    animation.save(OUT, writer=PillowWriter(fps=5.5), dpi=100)
    plt.close(fig)


if __name__ == "__main__":
    main()
