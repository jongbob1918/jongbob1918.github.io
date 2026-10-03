"""2장 '가중치 초기화' 표(LeCun, Xavier, He)를 방법마다 설명 그래프로 그린다.

각 방법은 평균이 0이고 분산이 정해진 분포에서 가중치를 뽑는다.
같은 분산이면 정규분포와 균등분포 모두 쓸 수 있고,
균등분포 U(-a, a)의 분산은 a^2 / 3 이므로 a = sqrt(3 * 분산) 이다.
왼쪽은 정규분포(표준편차), 오른쪽은 균등분포(양 끝 값)를 식으로 표시한다.

실행: python3 scripts/figures/ch02_init_methods.py
출력: site/public/images/notes/easy-deep-learning-ch02/init-{lecun,xavier,he}.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

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
plt.rcParams["axes.unicode_minus"] = False

# (파일명, 이름, 분산 식, 정규분포 표준편차 식, 균등분포 끝 값 식, 색)
METHODS = (
    ("lecun", "LeCun", "1/n_in", r"\sqrt{1/n_{in}}", r"\sqrt{3/n_{in}}", "#2f6fdb"),
    ("xavier", "Xavier", "2/(n_in+n_out)", r"\sqrt{2/(n_{in}+n_{out})}", r"\sqrt{6/(n_{in}+n_{out})}", "#e69f00"),
    ("he", "He", "2/n_in", r"\sqrt{2/n_{in}}", r"\sqrt{6/n_{in}}", "#2e9e5b"),
)
SIGMA = 1.0                 # 그림에서 표준편차를 1칸으로 둔다
HALF = np.sqrt(3) * SIGMA   # 같은 분산인 균등분포의 끝 값


def mark_ends(ax, pos, expr):
    """±pos 위치에 식을 바깥쪽으로 펼쳐 적는다(식이 길어도 겹치지 않게)."""
    ax.set_xticks([-pos, 0, pos])
    ax.set_xticklabels(["", "0", ""])
    trans = ax.get_xaxis_transform()
    ax.text(-pos, -0.07, f"-${expr}$", transform=trans, ha="right", va="top", fontsize=10)
    ax.text(pos, -0.07, f"${expr}$", transform=trans, ha="left", va="top", fontsize=10)


def draw(key, name, var_text, std_expr, edge_expr, color):
    fig, (ax_n, ax_u) = plt.subplots(1, 2, figsize=(8.4, 3.4), dpi=150, sharey=True)
    xlim = 2.6 * HALF

    # 왼쪽: 정규분포, 표준편차 위치를 표시
    x = np.linspace(-xlim, xlim, 800)
    pdf = np.exp(-x**2 / (2 * SIGMA**2)) / np.sqrt(2 * np.pi * SIGMA**2)
    ax_n.plot(x, pdf, color=color, lw=2.4)
    ax_n.fill_between(x, pdf, color=color, alpha=0.15)
    for s in (-SIGMA, SIGMA):
        ax_n.vlines(s, 0, np.exp(-0.5) / np.sqrt(2 * np.pi), color=color, ls="--", lw=1.3)
    mark_ends(ax_n, SIGMA, std_expr)
    ax_n.set_title("정규분포 (표준편차)", fontsize=11)

    # 오른쪽: 균등분포, 양 끝 값을 표시
    h = 1 / (2 * HALF)
    ax_u.plot([-xlim, -HALF, -HALF, HALF, HALF, xlim], [0, 0, h, h, 0, 0], color=color, lw=2.4)
    ax_u.fill_between([-HALF, HALF], [h, h], color=color, alpha=0.15)
    for s in (-HALF, HALF):
        ax_u.vlines(s, 0, h, color=color, ls="--", lw=1.3)
    mark_ends(ax_u, HALF, edge_expr)
    ax_u.set_title("균등분포 (양 끝 값)", fontsize=11)

    for ax in (ax_n, ax_u):
        ax.set_xlim(-xlim, xlim)
        ax.set_ylim(0, 0.5)
        ax.set_yticks([])
        ax.axvline(0, color="gray", lw=0.8)
        ax.spines[["top", "right", "left"]].set_visible(False)
    fig.suptitle(f"{name} 초기화: 분산 = {var_text}", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / f"init-{key}.png", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    for m in METHODS:
        draw(*m)
        print(m[1], "OK")
