"""Small fully connected network with one two-node path highlighted, matching
h = f1(w1 x + b1), y = f2(w2 h + b2) in the activation-function chapter.

Run: python3 scripts/figures/ch03_linear_network.py
Requires matplotlib.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch

for f in Path("/usr/share/fonts/truetype/nanum").glob("NanumGothic*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["mathtext.fontset"] = "dejavuserif"

OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/linear-nonlinear-activations"
ORANGE = "#e87924"
GRAY = "#94a3b8"
DARK = "#475569"
R = 0.42

X = [(0.0, 1.0), (0.0, -1.0)]
H = [(4.2, 2.0), (4.2, 0.0), (4.2, -2.0)]
O = [(8.4, 1.0), (8.4, -1.0)]
TAIL = 10.8


def arrow(ax, p, q, color, lw):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=1))


def circle(ax, p, s, color, fc="white", size=16):
    ax.add_patch(Circle(p, R, fc=fc, ec=color, lw=2.2, zorder=2))
    ax.text(*p, s, fontsize=size, ha="center", va="center",
            color=color if fc == "white" else "white", zorder=4)


def tag(ax, p, q, t, s, color, dy=0.0):
    x = p[0] + (q[0] - p[0]) * t
    y = p[1] + (q[1] - p[1]) * t + dy
    ax.text(x, y, s, fontsize=15, ha="center", va="center", color=color,
            bbox=dict(fc="white", ec="none", pad=1.5), zorder=5)


fig, ax = plt.subplots(figsize=(9.2, 5.2))
ax.set_aspect("equal")
ax.axis("off")

# every connection in gray; highlighted ones are drawn again on top
for p in X:
    for q in H:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.1, zorder=0)
for p in H:
    for q in O:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.1, zorder=0)
for q in O:
    arrow(ax, (q[0] + R, q[1]), (TAIL, q[1]), GRAY, 1.1)

# highlighted path: x1 -> f1 (top) -> f2 (top) -> y
ax.plot([X[0][0], H[0][0]], [X[0][1], H[0][1]], color=ORANGE, lw=3, zorder=1)
ax.plot([H[0][0], O[0][0]], [H[0][1], O[0][1]], color=ORANGE, lw=3, zorder=1)
arrow(ax, (O[0][0] + R, O[0][1]), (TAIL, O[0][1]), ORANGE, 3)

circle(ax, X[0], r"$x$", ORANGE)
circle(ax, X[1], r"$x$", GRAY)
ax.texts[-1].set_text(r"$x_2$")
ax.texts[-2].set_text(r"$x_1$")
circle(ax, H[0], r"$f_1$", ORANGE)
for p in H[1:]:
    circle(ax, p, r"$f_1$", GRAY)
circle(ax, O[0], r"$f_2$", ORANGE)
circle(ax, O[1], r"$f_2$", GRAY)

# labels on the highlighted path only
tag(ax, X[0], H[0], 0.45, r"$w_1$", ORANGE)
tag(ax, H[0], O[0], 0.55, r"$w_2$", ORANGE)
tag(ax, H[0], O[0], 0.17, r"$h$", ORANGE, dy=0.3)
ax.text(TAIL + 0.35, O[0][1], r"$y$", fontsize=17, color=ORANGE, ha="left", va="center")
for (cx, cy), name in ((H[0], r"$b_1$"), (O[0], r"$b_2$")):
    ax.text(cx - R - 0.1, cy + R + 0.05, name, fontsize=15, color=ORANGE,
            ha="right", va="bottom")

ax.set_xlim(-0.8, 11.8)
ax.set_ylim(-2.8, 3.4)
fig.tight_layout(pad=0.3)
fig.savefig(OUT / "linear-network-path.png", dpi=180, facecolor="white")
