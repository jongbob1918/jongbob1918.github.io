"""예측 p에 따라 MSE/BCE 기울기 그래프 위의 점이 움직이는 GIF.

실행: PYTHONDONTWRITEBYTECODE=1 python3 scripts/figures/ch05_backprop_animation.py
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from ch05_sigmoid_animation import set_korean_font

OUT=Path(__file__).resolve().parents[2]/'site/public/images/notes/easy-deep-learning-ch04/backprop-comparison.gif'
INK='#555555'; MSE='#c87529'; BCE='#2789ba'


def render():
    set_korean_font()
    plt.rcParams['mathtext.fontset']='cm'
    fig=plt.figure(figsize=(8,5.3),dpi=140,facecolor='white')
    grid=fig.add_gridspec(2,2,width_ratios=[1,1.5],left=.04,right=.96,top=.86,bottom=.12,wspace=.12,hspace=.55)
    labels=[fig.add_subplot(grid[i,0]) for i in range(2)]
    axes=[fig.add_subplot(grid[i,1]) for i in range(2)]
    p_grid=np.linspace(0,1,700)
    formulas=[r'$2(p-y)p(1-p)$',r'$p-y$']
    colors=[MSE,BCE]
    funcs=[lambda p:2*(p-1)*p*(1-p),lambda p:p-1]
    value_texts=[];dots=[];guides=[]
    fig.text(.05,.94,r'정답 $y=1$일 때',color=INK,fontsize=17)
    prediction=fig.text(.57,.94,r'예측값 $p=0.500$',color=INK,fontsize=22)
    for i,(left,ax,color,fn) in enumerate(zip(labels,axes,colors,funcs)):
        left.axis('off')
        left.text(.04,.87,['MSE','BCE'][i],color=color,fontsize=19,transform=left.transAxes)
        left.text(.04,.52,formulas[i],color=color,fontsize=24,transform=left.transAxes)
        value_texts.append(left.text(.04,.12,'',color=color,fontsize=25,transform=left.transAxes))
        ax.plot(p_grid,fn(p_grid),color=color,lw=2.4)
        ax.set(xlim=(-.025,1.025),ylim=(-1.06,.08),xticks=[0,.5,1],yticks=[-1,-.5,0])
        ax.spines[['top','right']].set_visible(False)
        for side in ['left','bottom']:ax.spines[side].set_color('#aaaaaa')
        ax.tick_params(colors=INK,labelsize=11)
        ax.axhline(0,color='#cccccc',lw=.7,zorder=0)
        ax.set_ylabel('기울기',color=INK,fontsize=12)
        guide,=ax.plot([.5,.5],[0,fn(.5)],color=color,lw=1,ls=(0,(3,3)),alpha=.65)
        dot,=ax.plot([.5],[fn(.5)],'o',color=color,markersize=8,mec='white',mew=1.5)
        guides.append(guide);dots.append(dot)
    axes[-1].set_xlabel('예측 p',color=INK,fontsize=12)
    frames=[]
    for frame in range(85):
        t=frame/84
        p=.5-.49*(t*t*(3-2*t))
        prediction.set_text(f'예측값 $p={p:.3f}$')
        for i,fn in enumerate(funcs):
            val=fn(p)
            value_texts[i].set_text(f'$= {val:.4f}$')
            dots[i].set_data([p],[val]);guides[i].set_data([p,p],[0,val])
        fig.canvas.draw()
        frames.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3]).convert('RGB'))
    durations=[100]*len(frames);durations[0]=1300;durations[-1]=3500
    palette=Image.fromarray(np.concatenate([np.asarray(frames[i]) for i in [0,42,84]],axis=0)).quantize(colors=128)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(OUT,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=False,disposal=2)
    frames[0].save('/tmp/ch05-animation-start.png')
    frames[-1].save('/tmp/ch05-animation-end.png')
    plt.close(fig)


if __name__=='__main__':render()
