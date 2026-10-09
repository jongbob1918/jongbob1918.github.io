"""다중분류 글의 softmax 계산, 범주형 분포, 교차 엔트로피 손실, 로짓 기울기 PNG를 만든다.

실행: python3 scripts/figures/ch06_multiclass.py
예시 로짓은 강아지·고양이·토끼 순서로 [2, 1, 0]이고, 정답은 강아지다.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

from ch05_sigmoid_animation import set_korean_font


OUT_DIR = Path(__file__).resolve().parents[2] / "site/public/images/notes/easy-deep-learning-ch05"
CLASSES = ["강아지", "고양이", "토끼"]
COLORS = ["#258978", "#e07b39", "#8b5bb5"]
LOGITS = np.array([2.0, 1.0, 0.0])
EXP = np.exp(LOGITS)
PROBS = EXP / EXP.sum()
ONE_HOT = np.array([1.0, 0.0, 0.0])
TEXT = "#292929"
assert np.allclose(PROBS.round(3), [0.665, 0.245, 0.090])


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#777777")
    ax.grid(axis="y", color="#e8ebee", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=12, colors="#444444")


def bars(ax, values, title, fmt, ymax):
    x = np.arange(len(CLASSES))
    ax.bar(x, values, width=0.62, color=COLORS)
    for xi, v in zip(x, values):
        ax.text(xi, v + ymax * 0.03, fmt.format(v), ha="center", va="bottom",
                fontsize=13, color=TEXT)
    ax.set(xticks=x, ylim=(0, ymax))
    ax.set_xticklabels(CLASSES)
    ax.set_title(title, fontsize=16, color=TEXT, pad=12)
    style(ax)


def arrow(fig, x0, x1, y, label):
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=18,
                                       color="#9aa2aa", linewidth=1.6))
    fig.text((x0 + x1) / 2, y + 0.05, label, ha="center", va="bottom",
             fontsize=12, color="#555555")


def softmax_example():
    fig, axes = plt.subplots(1, 3, figsize=(10, 4), dpi=200, facecolor="white",
                             gridspec_kw={"wspace": 0.55})
    fig.subplots_adjust(left=0.05, right=0.98, bottom=0.12, top=0.82)
    bars(axes[0], LOGITS, "로짓 z", "{:.0f}", 2.6)
    bars(axes[1], EXP, f"$e^z$  (합 {EXP.sum():.2f})", "{:.2f}", 9.6)
    bars(axes[2], PROBS, "확률 p  (합 1)", "{:.3f}", 0.87)
    for ax in axes:
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    arrow(fig, 0.315, 0.375, 0.47, "지수")
    arrow(fig, 0.645, 0.705, 0.47, "합으로\n나누기")
    fig.savefig(OUT_DIR / "softmax-example.png", facecolor="white")
    plt.close(fig)


def categorical_distribution():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200, facecolor="white",
                             gridspec_kw={"wspace": 0.25, "width_ratios": [3, 2]})
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.13, top=0.84)
    panels = (
        (axes[0], "범주형 분포 (K = 3)", CLASSES, PROBS, COLORS,
         [f"$p_{k + 1}$ = {v:.3f}" for k, v in enumerate(PROBS)]),
        (axes[1], "베르누이 분포 (K = 2)", ["불합격", "합격"], np.array([0.2, 0.8]),
         ["#e07b39", "#315f7d"], ["$1-p$ = 0.2", "$p$ = 0.8"]),
    )
    for ax, title, names, values, colors, labels in panels:
        x = np.arange(len(names))
        ax.bar(x, values, width=0.6, color=colors)
        for xi, v, label in zip(x, values, labels):
            ax.text(xi, v + 0.03, label, ha="center", va="bottom", fontsize=12, color=TEXT)
        ax.set(xticks=x, ylim=(0, 1.05), yticks=[0, 0.5, 1], xlim=(-0.6, len(names) - 0.4))
        ax.set_xticklabels(names)
        ax.set_title(title, fontsize=16, color=TEXT, pad=12)
        style(ax)
    axes[0].set_ylabel("확률", fontsize=14)
    fig.savefig(OUT_DIR / "categorical-distribution.png", facecolor="white")
    plt.close(fig)


def ce_loss_curve():
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=200, facecolor="white")
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.17, top=0.94)
    p = np.linspace(0.005, 1, 1000)
    ax.plot(p, -np.log(p), color="#315f7d", linewidth=2.8)
    for k, dx, dy in ((0, 0.04, 0.55), (2, 0.06, 0.25)):
        pc = PROBS[k]
        ax.scatter(pc, -np.log(pc), s=80, color=COLORS[k], zorder=3)
        ax.text(pc + dx, -np.log(pc) + dy,
                f"정답 {CLASSES[k]}: p = {pc:.3f}\n손실 ≈ {-np.log(pc):.3f}",
                fontsize=13, color=TEXT, va="bottom")
    ax.set(xlim=(0, 1.02), ylim=(0, 5.3), xticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
           yticks=range(6), xlabel="정답 클래스에 준 확률 $p_c$",
           ylabel="손실 $-\\ln p_c$")
    style(ax)
    ax.grid(color="#e8ebee", linewidth=0.7)
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    fig.savefig(OUT_DIR / "ce-loss-curve.png", facecolor="white")
    plt.close(fig)


def ce_gradient():
    grad = PROBS - ONE_HOT
    x = np.arange(len(CLASSES))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200, facecolor="white",
                             gridspec_kw={"wspace": 0.3})
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.2, top=0.86)

    ax = axes[0]
    ax.bar(x - 0.18, PROBS, width=0.34, color=COLORS, label="예측 $p_k$")
    ax.bar(x + 0.18, ONE_HOT, width=0.34, facecolor="none", edgecolor="#555555",
           linewidth=1.6, hatch="//", label="정답 $y_k$")
    for xi, v in zip(x, PROBS):
        ax.text(xi - 0.18, v + 0.03, f"{v:.3f}", ha="center", fontsize=11, color=TEXT)
    for xi, v in zip(x, ONE_HOT):
        ax.text(xi + 0.18, v + 0.03, f"{v:.0f}", ha="center", fontsize=11, color=TEXT)
    ax.set(xticks=x, ylim=(0, 1.18), yticks=[0, 0.5, 1])
    ax.set_xticklabels(CLASSES)
    ax.set_title("예측과 정답", fontsize=16, color=TEXT, pad=12)
    ax.legend(frameon=False, fontsize=12, loc="upper right")
    style(ax)

    ax = axes[1]
    ax.bar(x, grad, width=0.55, color=COLORS)
    ax.axhline(0, color="#777777", linewidth=1)
    for xi, g in zip(x, grad):
        ax.text(xi, g + (0.03 if g > 0 else -0.03), f"{g:+.3f}".replace("-", "−"), ha="center",
                va="bottom" if g > 0 else "top", fontsize=12, color=TEXT)
        ax.text(xi, -0.15, "로짓 ↑" if g < 0 else "로짓 ↓", ha="center", va="top",
                fontsize=13, color=COLORS[xi], transform=ax.get_xaxis_transform())
    ax.set(xticks=x, ylim=(-0.45, 0.4), yticks=[-0.4, -0.2, 0, 0.2, 0.4])
    ax.set_xticklabels(CLASSES)
    ax.tick_params(axis="x", length=0)
    ax.set_title("기울기 $p_k - y_k$", fontsize=16, color=TEXT, pad=12)
    style(ax)
    ax.spines["bottom"].set_visible(False)

    fig.savefig(OUT_DIR / "ce-gradient.png", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    set_korean_font()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    softmax_example()
    categorical_distribution()
    ce_loss_curve()
    ce_gradient()
