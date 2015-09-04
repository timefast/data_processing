# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 07:05:25 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

current_path = os.getcwd()
root = os.path.join(os.path.dirname(current_path),r'station')

all_data = pd.DataFrame()

for every_file in os.listdir(root):
    
    name_df=pd.read_csv(os.path.join(root,every_file),skiprows = 5,sep=' ').iloc[:,0]
    jingdu_df=pd.read_csv(os.path.join(root,every_file),skiprows = 5,sep=' ').iloc[:,1]
    fall_df=pd.read_csv(os.path.join(root,every_file),skiprows = 5,sep=' ').iloc[:,4]
    time_df = pd.DataFrame({'time': [str(every_file)[:8]] * len(name_df.index)})

    piece = [time_df,name_df,jingdu_df,fall_df]
    df = pd.concat(piece,axis=1,ignore_index=True)
    all_data = all_data.append(df,ignore_index = True)
     
def format_data(name,jingdu):
    if str(name)[:2] != '97':
        #format_name = str(name)
        first_name = str(name)[:2]
    elif jingdu > 114.25:
        #format_name = '0' + str(name)
        first_name = '0' + str(name)[:2]
    else:
        #format_name = '1' + str(name)
        first_name = '1' + str(name)[:2]
                 
    return first_name
    
format_data_ufunc = np.frompyfunc(format_data,2,1)
first_name = format_data_ufunc(all_data.loc[:,1],all_data.loc[:,2])
#format_name_df = pd.DataFrame(format_name)
first_name_df = pd.DataFrame(first_name)

piece = [all_data.loc[:,:1],first_name_df,all_data.loc[:,2:]]
all_data = pd.concat(piece,axis = 1,ignore_index = True)
df = all_data.replace(9999,np.nan)
df.to_csv('format_data.txt')
#print df
#i = 0
quyupingjun_result = []
zhanpingjun_result = []
for name,group in df.groupby(0):

    #group[group.loc[:,2].isin(['90','95','097'])].loc[:,4].to_csv(str(i) + '.txt')
    #i = i+1
    #print len(group.index)
    #print group[group.loc[:,2].isin(['90','95','097'])].loc[:,4].sum()
    #print group[group.loc[:,2].isin(['90','95','097'])].loc[:,4].sum() / len(group.index)
    hit = group.loc[:,2].isin(['90','95','097'])
    pingjun = group[hit].loc[:,4].sum() / len(group[hit].index)
    quyupingjun_result.append([name,pingjun])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])
    quyupingjun_result.append([])

###    print group[group.loc[:,4]>10].index

pd.DataFrame(quyupingjun_result).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'quyupingjun_result.txt')
    
for name,group in df.groupby(0):
#    group[group.loc[:,1].isin(['90','95','097'])].loc[:,4].to_csv(str(i) + '.txt')
#    i = i+1
#    print len(group.index)
#    print group[group.loc[:,1].isin(['90','95','097'])].loc[:,4].sum()
#    print group[group.loc[:,1].isin(['90','95','097'])].loc[:,4].sum() / len(group.index)
    hit = group.loc[:,1].isin([95043,95098,95151])
    #print  group[hit]
    pingjun = group[hit].loc[:,4].sum() / len(group[hit].index)
    zhanpingjun_result.append([name,pingjun])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
    zhanpingjun_result.append([])
       
#    print group[group.loc[:,4]>10].index

pd.DataFrame(zhanpingjun_result).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'zhanpingjun_result.txt')

print 'ok'