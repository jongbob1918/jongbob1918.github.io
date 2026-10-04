"""Draw gradient reuse using the chapter's green ReLU / blue linear network.

Run: python3 scripts/figures/ch04_reuse_gradients.py
Requires matplotlib. The PNG replaces the chapter's previous shared-delta figure.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site/public/images/notes/backpropagation/shared-delta.png"
for font in Path("/usr/share/fonts/truetype/nanum").glob("NanumGothic*.ttf"):
    font_manager.fontManager.addfont(str(font))
plt.rcParams.update({"font.family": "NanumGothic", "mathtext.fontset": "stix"})

GREEN, BLUE, ORANGE, RED = "#238443", "#2563EB", "#F58220", "#C94B43"
GRAY, INK = "#CBD2D9", "#222222"
fig, ax = plt.subplots(figsize=(14, 7))
fig.subplots_adjust(0, 0, 1, 1)
ax.set(xlim=(0, 1400), ylim=(0, 700), aspect="equal")
ax.axis("off")


def text(x, y, value, color=INK, size=18, **kwargs):
    return ax.text(x, y, value, color=color, fontsize=size, ha="center",
                   va="center", zorder=5, **kwargs)


def arrow(p, q, color=INK, width=1.2, head=True):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="->" if head else "-",
                                mutation_scale=12, color=color, lw=width,
                                shrinkA=0, shrinkB=0, zorder=1))


def node(x, y, label, color, fill, radius=23):
    ax.add_patch(Circle((x, y), radius, facecolor=fill, edgecolor=color,
                        lw=1.6, zorder=3))
    if label:
        text(x, y, label, color, size=12)


def network(offset, hidden=False):
    """Keep all 2-input / 3-hidden / 2-output nodes; emphasize only output 1."""
    def p(x, y):
        return x + offset, y

    for x, title, color in ((45, "입력층", INK), (250, "은닉층", GREEN),
                            (450, "출력층", BLUE), (590, "손실함수", RED)):
        text(*p(x, 592), title, color, 15)

    inputs, sums, hidden_ys, outputs = [505, 395], 180, [535, 460, 385], [505, 410]
    for i, iy in enumerate(inputs):
        for j, hy in enumerate(hidden_ys):
            hot = hidden and i == 0 and j == 0
            arrow(p(68, iy), p(sums - 4, hy), ORANGE if hot else GRAY,
                  2 if hot else 1)
    for j, hy in enumerate(hidden_ys):
        arrow(p(sums + 4, hy), p(227, hy), ORANGE if hidden and j == 0 else GRAY,
              2 if hidden and j == 0 else 1)
        arrow(p(273, hy), p(305, hy), ORANGE if j == 0 else GRAY,
              2 if j == 0 else 1, head=False)
        for k, oy in enumerate(outputs):
            hot = j == 0 and k == 0
            arrow(p(305, hy), p(390, oy), ORANGE if hot else GRAY,
                  2 if hot else 1)
    for k, oy in enumerate(outputs):
        arrow(p(390, oy), p(427, oy), ORANGE if k == 0 else GRAY,
              2 if k == 0 else 1)
        arrow(p(473, oy), p(521, oy), ORANGE if k == 0 else GRAY,
              2 if k == 0 else 1)
        node(*p(450, oy), r"$\mathrm{linear}$", BLUE if k == 0 else GRAY,
             "#E7EBFF" if k == 0 else "#F5F6F8")
        node(*p(390, oy), "", BLUE if k == 0 else GRAY, BLUE if k == 0 else GRAY, 3)
    for i, iy in enumerate(inputs, 1):
        node(*p(45, iy), rf"$x_{i}$", INK, "white")
    for j, hy in enumerate(hidden_ys):
        node(*p(250, hy), r"$\mathrm{ReLU}$" if j == 0 else "",
             GREEN if j == 0 else GRAY, "#E2F2E4" if j == 0 else "#F5F6F8")
        node(*p(sums, hy), "", GREEN if j == 0 else GRAY,
             GREEN if j == 0 else GRAY, 3)

    text(*p(99, 531), r"$w_1$", GREEN, 17,
         bbox=dict(fc="#E2F2E4" if hidden else "white",
                   ec=GREEN if hidden else "none", boxstyle="round,pad=0.2"))
    text(*p(100, 428), r"$w_2$", GREEN, 15)
    for x, y, label, color in ((178, 558, r"$+b_1$", GREEN),
                                (209, 552, r"$z_1$", GREEN),
                                (294, 552, r"$a_1$", GREEN),
                                (331, 553, r"$w_1$", BLUE),
                                (383, 529, r"$+b_1$", BLUE),
                                (408, 518, r"$z_1$", BLUE),
                                (513, 526, r"$\hat y_1$", BLUE)):
        text(*p(x, y), label, color, 16,
             bbox=dict(fc="#E7EBFF" if label == r"$w_1$" and not hidden else "white",
                       ec=BLUE if label == r"$w_1$" and not hidden else "none",
                       boxstyle="round,pad=0.1"))
    arrow(p(521, 505), p(543, 505), ORANGE, 2)
    ax.add_patch(FancyBboxPatch(p(548, 480), 83, 50, boxstyle="round,pad=0,rounding_size=9",
                               facecolor="#F2D4D1", edgecolor=RED, lw=1.5))
    text(*p(590, 505), r"$L$", RED, 22)


text(345, 658, "① 출력층 가중치의 미분", BLUE, 23, fontweight="bold")
text(1045, 658, "② 은닉층 가중치의 미분", GREEN, 23, fontweight="bold")
network(25)
network(725, hidden=True)

# Identical red boxes isolate dL/dyhat, not the full output-weight gradient.
def reuse_box(x, y, width=93, height=80):
    ax.add_patch(FancyBboxPatch((x - width / 2, y - height / 2), width, height,
                               boxstyle="round,pad=0,rounding_size=5",
                               facecolor="#FFF5F3", edgecolor=RED, lw=2))


reuse_box(338, 299)
reuse_box(958, 299)
text(210, 299, r"$\frac{\partial L}{\partial w_1}$", BLUE, 29)
text(269, 299, "$=$", size=25)
text(338, 299, r"$\frac{\partial L}{\partial\hat y_1}$", size=29)
text(403, 299, r"$\cdot$", size=25)
text(467, 299, r"$\frac{\partial\hat y_1}{\partial w_1}$", BLUE, 29)

text(830, 299, r"$\frac{\partial L}{\partial w_1}$", GREEN, 29)
text(890, 299, "$=$", size=25)
text(958, 299, r"$\frac{\partial L}{\partial\hat y_1}$", size=29)
for x in (1022, 1146, 1270):
    text(x, 299, r"$\cdot$", size=25)
for x, value, color in ((1084, r"$\frac{\partial\hat y_1}{\partial a_1}$", BLUE),
                         (1208, r"$\frac{\partial a_1}{\partial z_1}$", GREEN),
                         (1332, r"$\frac{\partial z_1}{\partial w_1}$", GREEN)):
    text(x, 299, value, color, 29)

arrow((338, 259), (338, 132), RED, 2, head=False)
arrow((338, 132), (958, 132), RED, 2, head=False)
arrow((958, 132), (958, 259), RED, 2)
text(648, 199, r"$\frac{\partial L}{\partial\hat y_1}=\hat y_1-y_1$", RED, 26)
text(648, 90, "출력층에서 구한 값을 그대로 재사용", RED, 20, fontweight="bold")

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=200, facecolor="white", metadata={"Description": "출력층과 은닉층 미분에서 손실의 예측값 미분을 재사용하는 계산 흐름"})
plt.close(fig)
