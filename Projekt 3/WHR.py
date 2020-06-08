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





def plot_Happiness(df:pd.DataFrame, byRegion:bool=False, topRange:int=20):
    if byRegion:
        df=df.groupby(['Region'])
        df.mean().head(topRange).sort_values('Happiness').plot.barh( y= 'Happiness', figsize=(20,10),title='Happiness of top '+  str(topRange)+' Regions')
    else:
        df.head(topRange).iloc[::-1].plot.barh( x='Country',y= 'Happiness', figsize=(20,10),title='Happiness of top '+  str(topRange)+' Countries')

def plot_Happiness_Detailed(df:pd.DataFrame, byRegion:bool=False,topRange:int=20): 
    if byRegion:
        ax=df.groupby(['Region']).mean().head(topRange).sort_values('Happiness').plot.barh(
                                               y=df.columns[4:],
                                               stacked=True,
                                               figsize=(20,10),
                                               title='Happiness in characteristics of top '+  str(topRange)+' Region')
        df.groupby(['Region']).mean().head(topRange).sort_values('Happiness').plot.barh(x='Region',
                                               y=df.columns[2],
                                               xerr=df.columns[3],
                                               stacked=True,
                                               ax=ax,
                                               alpha=0,
                                               label='_'
                                               )     
    else:
        ax=df.head(topRange).iloc[::-1].plot.barh(
                                               y=df.columns[4:],
                                               stacked=True,
                                               figsize=(20,10),
                                               title='Happiness in characteristics of top '+  str(topRange)+' Countries')
        df.head(topRange).iloc[::-1].plot.barh(x='Country',
                                               y=df.columns[2],
                                               xerr=df.columns[3],
                                               stacked=True,
                                               ax=ax,
                                               alpha=0,
                                               label='_'
                                               )
    
def GetRegion(df:pd.DataFrame,Countries:pd.Series)-> pd.Series:
    sr_Out=[]
    for country in Countries:
        sr_Out.append(str(df.loc[df.country==country]['Region indicator'].values))
    return sr_Out

def main():
    
    #read in data 
    df1 = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name=1 )
    df2 = pd.read_excel("WHR2018Chapter2OnlineData.xls", sheet_name=4 )
    
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
    #Add column 'Region'
    df1['Region']=GetRegion(df2,df1.Country.values)       
    cols=list(df1.columns)
    #sort cols
    df1=df1[[cols[-1]]+cols[0:2]+[cols[-2]]+cols[4:-2]]
    ##############################################
    plot_Happiness(df1,True)
    plot_Happiness_Detailed(df1,True,topRange=30)
    #print(df1.groupby(['Region']).mean().index)
    #print(df1.head(20))
    #df2_By_Regions=df2.groupby(['Region indicator']).mean()
    #
    #print(df1.columns)
    
if __name__ == "__main__":
    main()