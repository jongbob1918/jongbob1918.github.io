"""다중분류 글의 원-핫 인코딩 PNG를 만든다. 동물 사진마다 정답 자리만 1인 벡터를 붙인다.

실행: python3 scripts/figures/ch06_one_hot.py
사진 출처와 라이선스는 site/public/images/notes/easy-deep-learning-ch05/SOURCES.md에 있다.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from PIL import Image

from ch05_sigmoid_animation import set_korean_font


HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "site/public/images/notes/easy-deep-learning-ch05/one-hot-encoding.png"
CLASSES = ["강아지", "고양이", "토끼"]
# (사진 파일, 정사각형 자르기 영역 left, top, size의 원본 대비 비율)
PHOTOS = [
    ("ch06_dog.jpg", (0.0, 0.0, 1.0)),
    ("ch06_cat.jpg", (0.08, 0.12, 0.84)),
    ("ch06_rabbit.jpg", (0.0, 0.08, 1.0)),
]
BLACK = "#222222"
GRAY = "#9a9a9a"


def square(path, crop):
    img = Image.open(HERE / "photos" / path).convert("RGB")
    left, top, size = crop
    side = int(min(img.size) * size)
    x0, y0 = int(img.width * left), int(img.height * top)
    return img.crop((x0, y0, x0 + side, y0 + side)).resize((400, 400), Image.LANCZOS)


def main():
    set_korean_font()
    fig = plt.figure(figsize=(6.2, 6.2), dpi=200, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 6.2), ylim=(0, 6.2))
    ax.axis("off")

    cell, gap = 0.78, 0.12
    x_cells = 3.1
    ax.text(x_cells + 1.5 * cell + gap, 5.85, "정답 벡터", ha="center", va="center",
            fontsize=14, color=BLACK, weight="bold")
    for k, name in enumerate(CLASSES):
        ax.text(x_cells + k * (cell + gap) + cell / 2, 5.4, name, ha="center", va="center",
                fontsize=12, color="#555555")

    for row, (path, crop) in enumerate(PHOTOS):
        y = 3.75 - row * 1.75
        ax.imshow(square(path, crop), extent=(0.3, 1.8, y, y + 1.5), zorder=1)
        ax.add_patch(FancyArrowPatch((2.1, y + 0.75), (2.85, y + 0.75), arrowstyle="-|>",
                                     mutation_scale=18, color=GRAY, linewidth=1.6))
        for k in range(len(CLASSES)):
            x = x_cells + k * (cell + gap)
            hot = k == row
            ax.add_patch(Rectangle((x, y + 0.75 - cell / 2), cell, cell,
                                   facecolor=BLACK if hot else "white",
                                   edgecolor=BLACK if hot else "#c4c4c4", linewidth=1.2))
            ax.text(x + cell / 2, y + 0.75, "1" if hot else "0", ha="center", va="center",
                    fontsize=18, color="white" if hot else GRAY, weight="bold" if hot else None)

    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
