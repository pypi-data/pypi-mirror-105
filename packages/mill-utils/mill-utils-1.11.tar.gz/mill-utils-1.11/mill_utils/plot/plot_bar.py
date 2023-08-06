import matplotlib.patches as mpth
import matplotlib as mpl
import seaborn as sns
from matplotlib import pyplot as plt
def plot_bar(data,x,y,title=None,text_format='{:.3f}',labels = None
             ,xofsset=0.1,yofsset=0.5,figsize=(8,5),text_fontsize=12,title_fontsize=24
             ,bar_color=None,ax=None,cmap=None,maxwidth=lambda x:x*1.2,bbox_to_anchor=(0.8,0.99)):
    if ax==None:
        fig,ax = plt.subplots(figsize=figsize)
    sns.barplot(data=data,y=y,x=x,ax=ax)
    container = ax.containers[0]
    max_width = 0
    for i,t in enumerate(container):
        _,y = t.xy
        x = t.get_width()
        if x>max_width:
            max_width=x
        ax.text(x+xofsset,y+yofsset,text_format.format(x),fontsize=text_fontsize)
        if bar_color:
            t.set_color(cmap[bar_color(i,x)])
    if labels and cmap:
        handles = [mpth.Patch(color=cmap[x]) for x,t in enumerate(labels)]
        ax.legend(handles,labels,bbox_to_anchor=bbox_to_anchor)
    ax.set_xlim(0,maxwidth(max_width))
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title(title,fontsize=title_fontsize)