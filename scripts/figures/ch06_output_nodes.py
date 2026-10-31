"""기존 노드·원-핫 그림의 선과 흑백 스타일로 출력층 크기를 비교한다.

실행: python3 scripts/figures/ch06_output_nodes.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from ch05_sigmoid_animation import set_korean_font

OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch05/output-node-comparison.png"
DARK, GRAY = "#222222", "#b7b7b7"


def panel(ax, title, outputs, labels, target):
    ax.set(xlim=(-0.5, 4.5), ylim=(-0.8, 3.6), aspect="equal")
    ax.axis("off")
    ax.text(2, 3.3, title, ha="center", fontsize=16, weight="bold", color=DARK)
    ax.text(0.2, 2.65, "앞 층", ha="center", fontsize=11, color="#777777")
    ax.text(2.2, 2.65, f"출력층 · {len(outputs)}개", ha="center", fontsize=12, color=DARK)
    for y in [0.4, 1.3, 2.2]:
        for out_y in outputs:
            ax.plot([0.2, 2.2], [y, out_y], color=GRAY, lw=1, zorder=1)
        ax.add_patch(Circle((0.2, y), 0.21, fc="white", ec=GRAY, lw=1.4, zorder=2))
    for i, (y, label) in enumerate(zip(outputs, labels)):
        ax.add_patch(Circle((2.2, y), 0.26, fc="white", ec=DARK, lw=1.7, zorder=2))
        ax.text(2.2, y, "$z$" if len(outputs) == 1 else f"$z_{i+1}$",
                ha="center", va="center", fontsize=14, color=DARK)
        ax.text(2.65, y, label, va="center", fontsize=12, color=DARK)
    ax.text(2, -0.4, target, ha="center", fontsize=13, color=DARK)


def main():
    set_korean_font()
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.7), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98, wspace=0.1)
    panel(axes[0], "이진분류", [1.3], ["고양이 여부"], "정답 예: 1 (고양이)")
    panel(axes[1], "다중분류", [2.2, 1.3, 0.4], ["강아지", "고양이", "토끼"],
          "정답 예: [0, 1, 0]")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
