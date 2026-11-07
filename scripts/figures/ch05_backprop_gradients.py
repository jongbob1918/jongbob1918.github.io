"""역전파 계산 흐름과 출력층 기울기 비교 그림 생성.

실행: python3 scripts/figures/ch05_backprop_gradients.py
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from ch05_sigmoid_animation import set_korean_font, sigmoid

OUT = Path(__file__).resolve().parents[2] / 'site/public/images/notes/easy-deep-learning-ch04'
BLUE, ORANGE = '#315f7d', '#e6772e'


def render():
    set_korean_font()
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 3.5), dpi=200)
    ax.set(xlim=(0, 10), ylim=(0, 4))
    ax.axis('off')
    boxes = [(0.8, 2.65, '$x_1, x_2$\n입력'),
             (3.35, 2.65, '$z=w_1x_1+w_2x_2+b$\n점수'),
             (6.25, 2.65, '$p=\\sigma(z)$\n예측 확률'),
             (8.9, 2.65, '$L(p,y)$\n손실')]
    for x, y, label in boxes:
        ax.text(x, y, label, ha='center', va='center', fontsize=13,
                bbox=dict(boxstyle='round,pad=0.6', fc='#f1f5f8', ec=BLUE))
    for start, end in [(1.45, 2.0), (4.65, 5.5), (7.0, 8.2)]:
        ax.annotate('', (end, 2.65), (start, 2.65),
                    arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.8))
    ax.text(5, 3.7, '순전파: 입력에서 손실까지', ha='center', fontsize=14, color=BLUE)
    ax.annotate('', (2, 1.5), (9, 1.5),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))
    ax.text(5.5, 1.68, '역전파: 손실에서 가중치 쪽으로', ha='center', fontsize=13, color=ORANGE)
    ax.text(5, 0.5,
            r'$\frac{\partial L}{\partial w_1} = '
            r'\frac{\partial L}{\partial p}\;\times\;'
            r'\frac{\partial p}{\partial z}\;\times\;'
            r'\frac{\partial z}{\partial w_1}$',
            ha='center', va='center', fontsize=24)
    fig.tight_layout()
    fig.savefig(OUT / 'backprop-chain.png', facecolor='white')
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.9), dpi=200)
    z = np.linspace(-8, 8, 1000)
    p = sigmoid(z)
    axes[0].plot(z, p, color=BLUE, lw=2.5, label=r'$p=\sigma(z)$')
    axes[0].plot(z, p * (1-p), color=ORANGE, lw=2.5, label=r'$\partial p/\partial z=p(1-p)$')
    axes[0].set(title='시그모이드와 그 기울기', ylabel='함숫값', ylim=(-0.04, 1.08))
    axes[1].plot(z, 2*(p-1)*p*(1-p), color=ORANGE, lw=2.5, label='MSE')
    axes[1].plot(z, p-1, color=BLUE, lw=2.5, label='BCE')
    axes[1].set(title='정답 y = 1일 때 손실의 기울기', ylabel=r'$\partial L/\partial z$', ylim=(-1.08, 0.08))
    for a in axes:
        a.set(xlabel='점수 z', xlim=(-8, 8), xticks=[-8, -4, 0, 4, 8])
        a.spines[['top', 'right']].set_visible(False)
        a.grid(color='#e8ebee')
        a.set_axisbelow(True)
        a.legend(fontsize=10, loc='best')
    fig.tight_layout(pad=1.4)
    fig.savefig(OUT / 'backprop-gradients.png', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    render()
