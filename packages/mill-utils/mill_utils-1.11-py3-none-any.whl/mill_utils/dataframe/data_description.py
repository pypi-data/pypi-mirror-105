from matplotlib.colors import ListedColormap
from ..plot.plot_bar import plot_bar
from matplotlib.colors import ListedColormap
import pandas as pd
import numpy as np
'''
    查看数据的总体描述
'''

def bar_color(i,x):
	t= str(missing['dtype'][i])
	return labels.index(str(missing['dtype'][i]))    
    
class DataDescription:
    
    def __init__(self,data):
        self.data = data
        
    @property
    def desc_data(self):
        all_data=self.data
        desc_pd = pd.concat([all_data.nunique(),all_data.dtypes],axis=1,keys=('unique','dtype'))
        desc_pd = desc_pd.sort_values(by=['dtype','unique'])
        desc_pd = pd.concat([desc_pd,all_data.describe().T],axis=1)
        return desc_pd
    
    @property
    def desc_style_data(self):
        cmap = ListedColormap(sns.dark_palette('Green'))
        return self.desc_data.style.format('{:.2f}',subset=['count','mean','std','min','25%','50%','75%','max']).background_gradient(cmap=cmap,subset=['unique','std'])

    def desc_missing(self, zeroIsNull=False, showzero=False):
        '''
        显示缺失值情况
        '''
        data = self.data
        if zeroIsNull:
            missing = data.replace(0,np.NaN).isnull().sum().reset_index()
        else:
            missing = data.isnull().sum().reset_index()
        missing.columns = ['columns','miss_cnt']
        missing['proportion'] = missing['miss_cnt']/data.shape[0]
        missing = missing.sort_values('proportion',ascending=False)
        if not showzero:
            missing = missing.loc[missing['miss_cnt']>0,:]
        dtypes = data.dtypes.reset_index()
        dtypes.columns=['columns','dtype']
        missing = pd.merge(missing,dtypes,on='columns')
        return missing
    
    def plot_missing(self,zeroIsNull=False):
        '''
        绘制缺失值情况
        '''
        missing = self.desc_missing(zeroIsNull)
        labels = [str(x) for x in set(missing['dtype'])]
        cmap = [[0.8699104170307903, 0.6779079455577627, 0.6825747130218478],
             [0.6986365773597807, 0.436958338394959, 0.5850614007055088],
             [0.32163677087361386, 0.1892911785790927, 0.36408283626931454]]
        
        plot_bar(data=missing,y='columns',x='proportion',cmap=cmap,xofsset=0.02
             ,title="缺失值情况"
             ,bbox_to_anchor=(0.82,0.99)
             ,bar_color=lambda i,x:labels.index(str(missing['dtype'][i])),labels=labels,text_format='{:.2%}')
        pass
        
        