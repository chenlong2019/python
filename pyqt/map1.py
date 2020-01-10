import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Enable inline plotting

filelist = os.listdir(userdata) 
names = ['lat','lng','zero','alt','days','date','time']
df_list = [pd.read_csv(userdata + f,header=6,names=names,index_col=False) for f in filelist]
df = pd.concat(df_list, ignore_index=True)

# delete unused column
df.drop(['zero', 'days'], axis=1, inplace=True)

# data is recorded every 1~5 seconds, which is too frequent. Reduce it to every minute
df_min = df.iloc[::12, :]

df_min.head(10)