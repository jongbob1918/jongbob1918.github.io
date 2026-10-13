"""고양이 사진 한 장으로 데이터 증강 예시와 과한 증강 예시를 나란히 보여주는 PNG를 만든다.

원본은 scikit-image에 들어 있는 Chelsea 사진(CC0, Stefan van der Walt)이다.
왼쪽 3×2 칸은 고양이가 그대로 보이는 증강(잘라내기, 채도·명도, 비율, 좌우·상하 반전)이고,
오른쪽 한 열은 고양이가 사라지거나 다른 모양이 될 만큼 과한 증강이다.

실행: python3 scripts/figures/ch08_augmentation.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from skimage import data

from ch05_sigmoid_animation import set_korean_font


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch07/augmentation.png"
BLACK = "#222222"

W, H = 1.5, 1.0   # 칸 하나의 크기(원본 사진 비율 451:300)
GAP = 0.18
ROW_PITCH = H + 0.62  # 사진 + 아래 라벨 + 줄 간격
SPLIT = 0.7           # 적절한 증강과 과한 증강 사이 여백


def augmentations(cat):
    w, h = cat.size
    color = ImageEnhance.Brightness(ImageEnhance.Color(cat).enhance(0.35)).enhance(1.35)
    good = [
        ("원본", cat, 1.0),
        ("일부분 잘라내기", cat.crop((80, 50, 380, 250)).resize((w, h)), 1.0),
        ("채도·명도 변경", color, 1.0),
        ("비율 조절", cat, 0.75),
        ("좌우 반전", ImageOps.mirror(cat), 1.0),
        ("상하 반전", ImageOps.flip(cat), 1.0),
    ]
    bad = [
        ("배경만 남은 잘라내기", cat.crop((391, 160, 451, 200)).resize((w, h)), 1.0),
        ("너무 늘린 비율", cat, 0.3),
    ]
    return good, bad


def tile(ax, img, x, y, label, width_scale):
    # 비율 조절은 칸 높이는 그대로 두고 가로만 줄여, 같은 칸 안에서 모양이 변한 것을 보이게 한다
    w = W * width_scale
    x0 = x + (W - w) / 2
    ax.imshow(np.asarray(img), extent=(x0, x0 + w, y, y + H), zorder=2)
    ax.add_patch(plt.Rectangle((x0, y), w, H, fill=False, ec=BLACK, lw=0.8, zorder=3))
    ax.text(x + W / 2, y - 0.1, label, ha="center", va="top", fontsize=12, color=BLACK)


def render():
    set_korean_font()
    good, bad = augmentations(Image.fromarray(data.chelsea()))

    fig, ax = plt.subplots(figsize=(10.0, 4.6), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    ax.set_aspect("equal")
    x_bad = 3 * (W + GAP) - GAP + SPLIT
    top = ROW_PITCH + H
    ax.set(xlim=(-0.05, x_bad + W + 0.05), ylim=(-0.4, top + 0.42))
    ax.axis("off")

    for i, (label, img, scale) in enumerate(good):
        tile(ax, img, (i % 3) * (W + GAP), ROW_PITCH * (1 - i // 3), label, scale)
    for i, (label, img, scale) in enumerate(bad):
        tile(ax, img, x_bad, ROW_PITCH * (1 - i), label, scale)

    for x, title in ((0, "적절한 증강"), (x_bad, "과한 증강")):
        ax.text(x, top + 0.1, title, ha="left", va="bottom", fontsize=14, fontweight="bold", color=BLACK)
    divider = x_bad - SPLIT / 2
    ax.plot([divider, divider], [-0.3, top + 0.35], color="#cbd5e1", lw=1.2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render()
