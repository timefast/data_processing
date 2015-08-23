# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 07:47:55 2015

@author: Administrator
"""

import os
import pandas as pd
import numpy as np

current_path = os.getcwd()
root = os.path.join(os.path.dirname(current_path),'R/P')
outpath = os.path.join(os.path.dirname(current_path),'new_jiaodu/real_data_result')

all_jiaodu = pd.DataFrame()
all_sudu = pd.DataFrame()

all_time = []

#定义计算函数，用到数组的元素级别计算
def get_new_jiaodu(jiaodu):
    
    if float(jiaodu) < 270:
        new_jiaodu = 270 - float(jiaodu)
    else:
        new_jiaodu = 360 + 270 - float(jiaodu)
        
    return new_jiaodu

for every_file in os.listdir(root):
#每个文件取一列
    df_jiaodu=pd.read_csv(os.path.join(root,every_file),skiprows=3,header=None,nrows=99,sep=' ').iloc[:,1].replace('/////',np.nan)
    df_sudu=pd.read_csv(os.path.join(root,every_file),skiprows=3,header=None,nrows=99,sep=' ').iloc[:,2].replace('/////',np.nan)

    #print df_jiaodu
    array_jiaodu =df_jiaodu.values
    
    new_jiaodu_ufunc = np.frompyfunc(get_new_jiaodu, 1, 1)
    array_jiaodu = new_jiaodu_ufunc(array_jiaodu)
        #print U.dtype注意UV的类型为object
        #转换UV类型为float
    array_jiaodu = array_jiaodu.astype(np.float)
        #矩阵重新转为dataframe
    jiaodu_df = pd.DataFrame(array_jiaodu)
    
    all_jiaodu = all_jiaodu.append(jiaodu_df.T, ignore_index=True)
    all_sudu = all_sudu.append(df_sudu.T,ignore_index=True)
   
#解析文件名中所包含的日期并转换为datatime格式    
    time_index = pd.to_datetime(every_file.split('_')[4])
    all_time.append(time_index)
        
#把time作为index
all_jiaodu.index = all_time
all_sudu.index = all_time
#注意修改时间
rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')

all_time_jiaodu = all_jiaodu.reindex(rng)
all_time_sudu = all_sudu.reindex(rng)

all_time_jiaodu.to_csv(os.path.join(outpath,'real_alltime_new_jiaodu.txt'))
all_time_sudu.to_csv(os.path.join(outpath,'real_alltime_sudu.txt'))