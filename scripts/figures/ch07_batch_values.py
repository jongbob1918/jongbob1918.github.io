"""노드 하나의 배치 값을 ReLU 그래프 위에 빨간 눈금으로 표시한 PNG 두 장을 만든다.

1. batch-values-relu.png: 배치 정규화 없이 값 3, 9, 11, 17이 ReLU로 들어간다.
2. batch-values-batchnorm.png: 배치 정규화를 거친 -1.4, -0.2, 0.2, 1.4가 ReLU로 들어간다.

배치의 샘플은 같은 노드를 각각 따로 지나므로, 값들은 합쳐지지 않고 한 열(벡터)로 함께 움직인다.

3. layer-values-layernorm.png: 한 샘플의 노드 4개 값이 레이어 정규화를 거쳐 ReLU로 들어간다.

실행: python3 scripts/figures/ch07_batch_values.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

from ch05_sigmoid_animation import set_korean_font


OUT_DIR = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch06"
CURVE = "#315f7d"
ORANGE = "#e87924"
DARK = "#334155"
GRAY = "#94a3b8"
RED = "#dc2626"

BATCH = [3, 9, 11, 17]
NORMALIZED = [-1.4, -0.2, 0.2, 1.4]
YS = [1.65, 0.55, -0.55, -1.65]
X_COL = 2.2
X_BN_L, X_BN_R = 4.7, 6.4
CENTER = (10.0, 0.0)
R = 3.0
HALF = 0.66 * R  # 원 안에 들어가는 그래프 영역의 반변 길이


def arrow(ax, x0, x1, y=0.0):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=18,
                                 color=GRAY, lw=2.2, shrinkA=0, shrinkB=0, zorder=1))


def bracket(ax, x, side, y0=-2.25, y1=2.25, tick=0.18):
    sign = 1 if side == "left" else -1
    ax.plot([x + sign * tick, x, x, x + sign * tick], [y1, y1, y0, y0],
            color=DARK, lw=2.2, solid_capstyle="butt", zorder=2)


# 정규화 전후 그래프 크기와 눈금 범위를 똑같이 두어 분포가 얼마나 모였는지 비교한다.
X_LO, Y_LO, SPAN = -18, -18, 36


def relu_circle(ax, values, fmt, label_offsets=None):
    """원 안에 ReLU 그래프를 그리고 값의 위치를 빨간 눈금으로 표시한다.

    x, y 눈금 간격을 같게 해서 양수 구간의 기울기가 1(45도)로 보이게 한다.
    눈금끼리 가까워 숫자가 겹칠 때는 label_offsets로 숫자를 옮기고 선으로 잇는다.
    """
    cx, cy = CENTER
    x_hi, y_hi = X_LO + SPAN, Y_LO + SPAN
    ax.add_patch(Circle(CENTER, R, fc="white", ec=CURVE, lw=3, zorder=3))

    def px(x):
        return cx - HALF + (x - X_LO) / SPAN * 2 * HALF

    def py(y):
        return cy - HALF + (y - Y_LO) / SPAN * 2 * HALF

    end = min(x_hi, y_hi)
    ax.plot([px(X_LO), px(x_hi)], [py(0), py(0)], color=GRAY, lw=1.4, zorder=4)
    ax.plot([px(0), px(0)], [py(0), py(y_hi)], color=GRAY, lw=1.4, zorder=4)
    ax.plot([px(X_LO), px(0), px(end)], [py(0), py(0), py(end)], color=CURVE, lw=3.2,
            solid_joinstyle="round", zorder=5)

    label_y = py(0) - 0.7
    for i, v in enumerate(values):
        x = px(v)
        ax.plot([x, x], [py(0) - 0.2, py(0) + 0.2], color=RED, lw=1.8,
                solid_capstyle="butt", zorder=7)
        if label_offsets is None:
            lx = x
        else:
            lx = px(0) + label_offsets[i]
            ax.plot([x, lx], [py(0) - 0.2, label_y + 0.22], color=RED, lw=1, zorder=6)
        # 눈금끼리 가까울 때(선으로 잇지 않는 경우) 숫자를 번갈아 두 줄로 놓는다
        dy = -0.42 if label_offsets is None and i % 2 else 0
        ax.text(lx, label_y + dy, fmt(v), ha="center", va="center",
                fontsize=14, fontweight="bold", color=RED, zorder=7)


def column(ax):
    bracket(ax, X_COL - 0.65, "left")
    bracket(ax, X_COL + 0.65, "right")
    for i, (v, y) in enumerate(zip(BATCH, YS), start=1):
        ax.text(X_COL, y, str(v), ha="center", va="center", fontsize=21,
                fontweight="bold", color=CURVE, zorder=3)
        ax.text(X_COL - 0.95, y, f"샘플 {i}", ha="right", va="center", fontsize=13, color="#64748b")
    ax.text(X_COL - 0.2, 2.8, "한 노드의 배치 값", ha="center", va="center", fontsize=15, color=DARK)


def render(name, with_bn, values, fmt, label_offsets=None):
    fig, ax = plt.subplots(figsize=(10.72, 5.44), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
    ax.set_aspect("equal")
    ax.set(xlim=(0, 13.4), ylim=(-3.4, 3.4))
    ax.axis("off")

    column(ax)
    if with_bn:
        arrow(ax, X_COL + 0.85, X_BN_L - 0.03)
        ax.add_patch(FancyBboxPatch((X_BN_L, -2.25), X_BN_R - X_BN_L, 4.5,
                                    boxstyle="round,pad=0.02,rounding_size=0.35",
                                    fc="#fff4e8", ec=ORANGE, lw=2.6, zorder=2))
        ax.text((X_BN_L + X_BN_R) / 2, 0, "배치\n정규화", ha="center", va="center",
                fontsize=18, fontweight="bold", color=ORANGE, linespacing=1.4, zorder=4)
        arrow(ax, X_BN_R + 0.03, CENTER[0] - R - 0.03)
    else:
        arrow(ax, X_COL + 0.85, CENTER[0] - R - 0.03)

    relu_circle(ax, values, fmt, label_offsets)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / name, facecolor="white")
    plt.close(fig)


def render_layernorm(name, values, fmt, label_offsets):
    """레이어 정규화: 한 샘플이 노드 4개에서 낸 값이 모듈 하나로 함께 들어간다."""
    fig, ax = plt.subplots(figsize=(10.72, 5.44), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
    ax.set_aspect("equal")
    ax.set(xlim=(0, 13.4), ylim=(-3.4, 3.4))
    ax.axis("off")

    x_node, node_r = 2.2, 0.45
    for i, (v, y) in enumerate(zip(BATCH, YS), start=1):
        ax.text(x_node - 0.75, y, f"노드 {i}", ha="right", va="center", fontsize=13, color="#64748b")
        ax.add_patch(Circle((x_node, y), node_r, fc="white", ec=CURVE, lw=2.4, zorder=3))
        p, q = (x_node + node_r + 0.03, y), (X_BN_L - 0.03, y)
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=GRAY,
                                     lw=2, shrinkA=0, shrinkB=0, zorder=1))
        ax.text((p[0] + q[0]) / 2, y, str(v), ha="center", va="center", fontsize=19,
                fontweight="bold", color=CURVE, bbox=dict(fc="white", ec="none", pad=2.5), zorder=5)
    ax.text(x_node - 0.2, 2.8, "한 샘플의 노드 값", ha="center", va="center", fontsize=15, color=DARK)

    ax.add_patch(FancyBboxPatch((X_BN_L, -2.25), X_BN_R - X_BN_L, 4.5,
                                boxstyle="round,pad=0.02,rounding_size=0.35",
                                fc="#fff4e8", ec=ORANGE, lw=2.6, zorder=2))
    ax.text((X_BN_L + X_BN_R) / 2, 0, "레이어\n정규화", ha="center", va="center",
            fontsize=18, fontweight="bold", color=ORANGE, linespacing=1.4, zorder=4)
    arrow(ax, X_BN_R + 0.03, CENTER[0] - R - 0.03)

    relu_circle(ax, values, fmt, label_offsets)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / name, facecolor="white")
    plt.close(fig)


def main():
    set_korean_font()
    render("batch-values-relu.png", False, BATCH, lambda v: f"{v:g}")
    render("batch-values-batchnorm.png", True, NORMALIZED,
           lambda v: f"{v:g}".replace("-", "−"), label_offsets=[-1.05, -0.35, 0.35, 1.05])
    render_layernorm("layer-values-layernorm.png", NORMALIZED,
                     lambda v: f"{v:g}".replace("-", "−"), [-1.05, -0.35, 0.35, 1.05])


if __name__ == "__main__":
    main()
