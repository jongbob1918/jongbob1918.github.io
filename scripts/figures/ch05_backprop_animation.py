"""MSE/BCE의 역전파를 비교하는 GIF. 실행: PYTHONDONTWRITEBYTECODE=1 python3 scripts/figures/ch05_backprop_animation.py"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from ch05_sigmoid_animation import set_korean_font

OUT=Path(__file__).resolve().parents[2]/'site/public/images/notes/easy-deep-learning-ch04/backprop-comparison.gif'
BG='#ffffff'; INK='#555555'; MSE='#c87529'; BCE='#2789ba'; FACTOR='#a17b1e'

def render():
    set_korean_font()
    plt.rcParams['mathtext.fontset']='cm'
    fig,ax=plt.subplots(figsize=(7.2,4.8),dpi=140)
    frames=[]
    def text(x,y,s,c=INK,size=18,alpha=1):
        ax.text(x,y,s,ha='center',va='center',color=c,fontsize=size,alpha=alpha)
    def clamp(x):return max(0,min(1,x))
    for frame in range(120):
        t=frame/119
        u=clamp((t-.1)/.42);u=u*u*(3-2*u)
        p=.5-.49*u;s=p*(1-p);m=2*(p-1);b=(p-1)/s
        ax.clear();ax.set(xlim=(0,720),ylim=(0,480));ax.axis('off')
        text(100,451,r'정답 $y=1$',size=17)
        text(550,451,f'$p={p:.4f}$',size=23)
        ax.plot([100,620],[417,417],color='#cccccc',lw=1)
        ax.scatter([100+520*p],[417],s=45,color=FACTOR,zorder=5)
        text(100,395,'0',size=11);text(620,395,'1',size=11)
        text(280,359,'손실 함수의 기울기',size=13)
        text(500,359,'시그모이드의 기울기',size=13)
        text(70,310,'MSE',MSE,18)
        text(280,315,r'$2(p-y)$',MSE,24)
        text(400,315,r'$\times$',size=23)
        text(500,315,r'$p(1-p)$',FACTOR,24)
        text(280,275,f'{m:.2f}',MSE,16)
        text(500,275,f'{s:.4f}',FACTOR,16)
        text(70,207,'BCE',BCE,18)
        text(280,232,r'$p-y$',BCE,24)
        ax.plot([220,340],[211,211],color=INK,lw=1)
        text(280,190,r'$p(1-p)$',FACTOR,24)
        text(400,211,r'$\times$',size=23)
        text(500,211,r'$p(1-p)$',FACTOR,24)
        text(280,151,f'{b:.2f}',BCE,16)
        text(500,151,f'{s:.4f}',FACTOR,16)
        c=clamp((t-.57)/.12)
        if c>0:
            for x,y in [(220,175),(440,196)]:
                ax.plot([x,x+120*c],[y,y+30*c],color='#c55b60',lw=2)
        text(638,211,r'$=p-y$',BCE,23,clamp((t-.69)/.07))
        a=clamp((t-.78)/.08)
        if a>0:
            text(114,97,'전달되는 기울기',size=12,alpha=a)
            text(114,74,'길이 = 절댓값',size=10,alpha=a)
            for y,label,v,color in [(96,'MSE',m*s,MSE),(45,'BCE',p-1,BCE)]:
                text(230,y,label,color,13,a)
                ax.plot([280,600],[y-13,y-13],color='#dddddd',lw=1,alpha=a)
                ax.barh(y,320*abs(v),left=280,height=15,color=color,alpha=a)
                text(656,y,f'{v:.4f}',color,14,a)
        fig.subplots_adjust(left=.01,right=.99,top=.99,bottom=.01)
        fig.canvas.draw()
        frames.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3]).convert('RGB'))
    # Pause on the initial state and final comparison; no fast reset flash.
    durations=[100]*len(frames);durations[0]=1200;durations[-1]=3500
    palette=Image.fromarray(np.concatenate([np.asarray(frames[i]) for i in [0,60,119]],axis=0)).quantize(colors=128)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(OUT,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=False,disposal=2)
    frames[60].save('/tmp/ch05-animation-middle.png')
    frames[-1].save('/tmp/ch05-animation-end.png')
    plt.close(fig)

if __name__=='__main__':render()
