"""2장 '가중치 초기화' 절의 n_in, n_out을 보여 주는 간단한 신경망 그림.

앞 층 노드 3개와 다음 층 노드 4개를 연결하고, 다음 층의 한 노드로 들어오는
연결(= n_in)과 다음 층의 노드 수(= n_out)를 표시한다.

실행: python3 scripts/figures/ch02_nin_nout.py
출력: site/public/images/notes/easy-deep-learning-ch02/nin-nout-diagram.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle

OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch02"

FONT_FILES = (
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgun.ttf",
)
for path in FONT_FILES:
    if Path(path).exists():
        font_manager.fontManager.addfont(path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
        break

LEFT_X, RIGHT_X, R = 0.0, 4.0, 0.3
LEFT_Y = [2.0, 1.0, 0.0]            # 앞 층: n_in = 3
RIGHT_Y = [2.5, 1.5, 0.5, -0.5]     # 다음 층: n_out = 4
HIGHLIGHT = 1                       # 강조할 다음 층 노드
BLUE, ORANGE, GRAY = "#2f6fdb", "#e8710a", "#b0b0b0"


def main():
    fig, ax = plt.subplots(figsize=(9, 3.4), dpi=150)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-4.6, 7.4)
    ax.set_ylim(-1.1, 3.6)

    for j, ry in enumerate(RIGHT_Y):
        for ly in LEFT_Y:
            hl = j == HIGHLIGHT
            ax.plot([LEFT_X + R, RIGHT_X - R], [ly, ry], color=ORANGE if hl else GRAY,
                    lw=2.4 if hl else 1.0, alpha=1 if hl else 0.6, zorder=1)

    for ly in LEFT_Y:
        ax.add_patch(Circle((LEFT_X, ly), R, fc="white", ec=BLUE, lw=2, zorder=2))
    for j, ry in enumerate(RIGHT_Y):
        ax.add_patch(Circle((RIGHT_X, ry), R, fc="#fff4e6" if j == HIGHLIGHT else "white",
                            ec=ORANGE if j == HIGHLIGHT else BLUE, lw=2, zorder=2))

    ax.text(LEFT_X, 3.2, "앞 층", ha="center", fontsize=11)
    ax.text(RIGHT_X, 3.2, "다음 층", ha="center", fontsize=11)

    # n_out: 다음 층의 노드 수 (오른쪽 세로 괄호)
    ax.annotate("", xy=(RIGHT_X + 0.7, 2.8), xytext=(RIGHT_X + 0.7, -0.8),
                arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.6))
    ax.text(RIGHT_X + 0.95, 1.0, r"$n_{out}$ = 4" "\n(다음 층의 노드 수)", va="center",
            fontsize=11, color=BLUE)

    # n_in: 다음 층의 한 노드로 들어오는 연결 수 (왼쪽 세로 괄호)
    ax.annotate("", xy=(LEFT_X - 0.7, 2.3), xytext=(LEFT_X - 0.7, -0.3),
                arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.6))
    ax.text(LEFT_X - 0.95, 1.0, r"$n_{in}$ = 3" "\n(앞 층의 노드 수\n= 한 노드로 들어오는 연결 수)",
            va="center", ha="right", fontsize=11, color=ORANGE)

    fig.tight_layout()
    fig.savefig(OUT / "nin-nout-diagram.png", facecolor="white")


if __name__ == "__main__":
    main()
