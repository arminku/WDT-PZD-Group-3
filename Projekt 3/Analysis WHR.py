# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 11:23:41 2020

@author: ArminK
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Data= pd.read_excel("WHR2018Chapter2OnlineData.xls")

#print(Data.groupby(by=['country']).count())
#GroupByCountry=Data.groupby(by=['country']).mean()
#CountryData= for country in Data.Country
#DataByYears=
#info=Data.info()
#Description=Data.describe()
#fig=Data.hist(figsize=(30,40),bins=50, xlabelsize=15, ylabelsize=15)
#[x.title.set_size(18) for x in fig.ravel()]
#fig=plt.figure(figsize=(25,10))
#for column in Data.columns
 #   fig.add_subplot(Dat[column])
#corr = Data.corr()
plt.figure()
#axs=fig.
#sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, cmap=sns.diverging_palette(220, 10, as_cmap=True))

#print(CleanedData.head())
def sortbyYear():
    Data.columns=Data.columns.str.strip()
    Data.sort_values(by='year',inplace=True)
    #Data.set_index(keys=['year'],drop=False, inplace=True)
sortbyYear()    
Years=Data.year.unique().tolist()

#DataByYears=Data.loc[Data.year==2017]


def sortbyCountry():
 #   Data.columns=Data.columns.str.strip()
    Data.sort_values(by='country',inplace=True)
    #Data.set_index(keys=['country'],drop=False, inplace=True)
sortbyCountry()
Countries=Data.country.unique().tolist()

#DataByYears=Data.loc[Data.year==2017]

#print(np.sort(Data.year.unique()))
#DataByYears=[]
sns.reset_defaults()
sns.set(
    rc={'figure.figsize':(5,5)}, 
    style="white" # nicer layout
)
sns_data={}
for column in Data.columns:
    sns_data[column]= Data[(Data['country']=='Germany') & (Data[column])]
    sns.scatterplot(
            sns_data[column]['year'],
            label=column
            )
plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
sns.despine()
#sns_data=Data[(Data['country']=='Germany') & (Data['year']==2015)]
#sns.kdeplot(
#            sns_data['Life Ladder'],
#           label='Life Ladder'
#           )
#sns.despine()
                    