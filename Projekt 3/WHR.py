# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:42:01 2020

@author: ArminK
"""


import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import colors as mcolors

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)





def plot_Happiness(df:pd.DataFrame, topRange:int=20):
    df.head(topRange).iloc[::-1].plot.barh( x='Country',y= 'Happiness', figsize=(20,10))

def plot_Happiness_Detailed(df:pd.DataFrame, topRange:int=20): 
    
    ax=df.head(topRange).iloc[::-1].plot.barh(x='Country',
                                               y=df.columns[3:],
                                               stacked=True,
                                               figsize=(20,10))
    df.head(topRange).iloc[::-1].plot.barh(x='Country',
                                               y=df.columns[1],
                                               xerr=df.columns[2],
                                               stacked=True,
                                               ax=ax,
                                               alpha=0,
                                               label='_'
                                               )

def main():
    
    #read in data 
    df1 = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name=1 )
    
    #################Clean up sheet 1#####################
    #delete empty columns
    df1= df1.iloc[0:-1 , 0:11]      
    #clean up column names
    df1.columns=['Country','Happiness','95% conf. max', 
            '95% conf. min', 'Dystopia+Res.',
            'GDP/capita', 'Social sup.',
            'Healthy life exp.', 'Freedom of choices',
            'Generosity','Perc. of corr.']   
    #clean up 95% conf to 1 columns "error"
    df1['error']=df1['Happiness']-df1['95% conf. min']   
    cols=list(df1.columns)
    #sort cols
    df1=df1[cols[0:2]+[cols[-1]]+cols[4:-1]]
    ##############################################
    #plot_Happiness(df)
    plot_Happiness_Detailed(df1,30)
    
if __name__ == "__main__":
    main()