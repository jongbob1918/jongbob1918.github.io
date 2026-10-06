"""고정된 동전 관측 순서에 대한 두 확률 후보의 우도를 비교한다.

실행: python3 scripts/figures/ch05_coin_likelihood.py
관측 순서는 설명용 예시이며 앞면 7번, 뒷면 3번이다.
순서를 고정한 우도 p**7 * (1-p)**3을 사용한다.
앞면 개수만 관측했을 때의 이항 확률과는 구분한다.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch04/coin-likelihood.png"
OBSERVATIONS = [1, 1, 0, 1, 1, 0, 1, 1, 1, 0]
HEADS, TAILS = sum(OBSERVATIONS), len(OBSERVATIONS) - sum(OBSERVATIONS)
assert (HEADS, TAILS) == (7, 3)


def render():
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
    fig = plt.figure(figsize=(8, 5.2), dpi=200, facecolor="white")
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set(xlim=(0, 1000), ylim=(0, 650), aspect="equal")
    ax.axis("off")
    text_color = "#292929"
    ax.text(500, 586, "앞면 7번 · 뒷면 3번", fontsize=20,
            ha="center", va="center", color=text_color)
    for i, head in enumerate(OBSERVATIONS):
        x = 95 + i * 90
        fill, edge = ("#ffe4a0", "#bb8a29") if head else ("#e3e8ed", "#8c97a2")
        ax.add_patch(Circle((x, 500), 31, facecolor=fill, edgecolor=edge, linewidth=1.5))
        ax.add_patch(Circle((x, 500), 25, facecolor="none", edgecolor=edge, linewidth=0.6))
        ax.text(x, 500, "앞" if head else "뒤", fontsize=18,
                ha="center", va="center", color=text_color)
    ax.add_patch(FancyArrowPatch((500, 443), (500, 391), arrowstyle="-|>",
                                mutation_scale=17, color="#b8bec5", linewidth=1.3))
    ax.text(500, 358, "이 순서가 나올 우도", fontsize=17,
            ha="center", va="center", color=text_color)
    for p, y, color in ((0.5, 270, "#8b5bb5"), (0.7, 155, "#258978")):
        likelihood = p ** HEADS * (1 - p) ** TAILS
        width = likelihood / 0.0025 * 555
        ax.text(112, y, f"p = {p:.1f}", fontsize=21, color=text_color,
                ha="left", va="center")
        ax.add_patch(FancyBboxPatch((310, y - 23), width, 46,
                                   boxstyle="round,pad=0,rounding_size=9",
                                   facecolor=color, edgecolor="none"))
        ax.text(310 + width + 17, y, f"{likelihood:.5f}", fontsize=17,
                color=text_color, ha="left", va="center")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
