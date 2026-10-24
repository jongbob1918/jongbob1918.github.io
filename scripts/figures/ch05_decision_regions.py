"""퍼셉트론의 출력 영역 예시: z = 10x1 + x2 - 100."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from ch05_linear_classification import configure_font


def main():
    configure_font()
    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=200)
    x = np.linspace(0, 10, 201)
    boundary = 100 - 10 * x
    ax.fill_between(x, boundary, 100, color='#e1edf5')
    ax.fill_between(x, 0, boundary, color='#fbeadb')
    ax.plot(x, boundary, color='#675084', lw=2.5)
    ax.text(6.8, 79, '출력 1\n$z > 0$', ha='center', va='center', color='#315a7a', fontsize=17)
    ax.text(2.7, 23, '출력 0\n$z < 0$', ha='center', va='center', color='#a75522', fontsize=17)
    ax.scatter([5], [50], s=65, color='#675084', zorder=3)
    ax.annotate('경계에서도 출력 0\n$z = 0$', xy=(5, 50), xytext=(6.4, 49),
                fontsize=12, va='center', arrowprops={'arrowstyle': '-', 'color': '#675084'})
    ax.text(1.3, 91, '$x_2 = -10x_1 + 100$', fontsize=14, color='#675084',
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': .9})
    ax.set(xlim=(0, 10), ylim=(0, 100), xlabel='공부 시간 $x_1$ (시간)', ylabel='출석률 $x_2$ (%)')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(color='white', alpha=.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    out = Path(__file__).resolve().parents[2] / 'site/public/images/notes/easy-deep-learning-ch04/perceptron-decision-regions.png'
    fig.savefig(out, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    main()
