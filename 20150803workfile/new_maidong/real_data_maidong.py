﻿# -*- coding: utf-8 -*-
"""
Created on Sun Aug 02 16:51:58 2015

@author: Administrator
"""
####修改路径，修改时间end多加一个小时，修改实际时间的范围（3处需要修改）
import os
import pandas as pd
import numpy as np
from datetime import datetime

current_path = os.getcwd()
root = os.path.join(os.path.dirname(current_path),'R/P')

outpath = os.path.join(os.path.dirname(current_path),'new_maidong/real_data_result')


all_U = pd.DataFrame()
all_V = pd.DataFrame()
all_chuizhi = pd.DataFrame()

all_time = []

#定义计算函数，用到数组的元素级别计算
def calUV(jiaodu,sudu):

    u = (-1) * np.sin( float(jiaodu) * np.pi / 180) * float(sudu)
    v = (-1) * np.cos( float(jiaodu) * np.pi / 180) * float(sudu)

    return '%.2f' % u,'%.2f' % v
    
for every_file in os.listdir(root):

#每个文件取一列
    df_jiaodu=pd.read_csv(os.path.join(root,every_file),skiprows=3,header=None,nrows=99,sep=' ').iloc[:,1].replace('/////',np.nan)
    array_jiaodu =df_jiaodu.values
    
    df_sudu=pd.read_csv(os.path.join(root,every_file),skiprows=3,header=None,nrows=99,sep=' ').iloc[:,2].replace('/////',np.nan)
    array_sudu = df_sudu.values
    df_chuizhi=pd.read_csv(os.path.join(root,every_file),skiprows=3,header=None,nrows=99,sep=' ').iloc[:,3].replace('/////',np.nan)
    
    calUV_ufunc = np.frompyfunc(calUV, 2, 2)
    [U, V] = calUV_ufunc(array_jiaodu,array_sudu)
        #print U.dtype注意UV的类型为object
        #转换UV类型为float
    U = U.astype(np.float)
    V = V.astype(np.float)

        #矩阵重新转为dataframe
    Udf = pd.DataFrame(U)
    Vdf = pd.DataFrame(V)
    
    all_U = all_U.append(Udf.T, ignore_index=True)
    all_V = all_V.append(Vdf.T, ignore_index=True)
    
    all_chuizhi = all_chuizhi.append(df_chuizhi.T, ignore_index=True)
    
#解析文件名中所包含的日期并转换为datatime格式    
    time_index = pd.to_datetime(every_file.split('_')[4])
    all_time.append(time_index)
        
#把time作为index
all_U.index = all_time
all_V.index = all_time
all_chuizhi.index = all_time

#注意修改时间，end多加一个小时
#生成日期范围
rng = pd.date_range(start = '20130628000000', end = '20130630010000', freq='5min')
#reindex从而实现日期范围内未有的部分全部插空值
all_time_U = all_U.reindex(rng)
all_time_V = all_V.reindex(rng)
all_time_chuizhi = all_chuizhi.reindex(rng)

all_time_U.replace(np.nan,9999).to_csv(os.path.join(outpath,'all_time_U.txt'),sep = ' ')
all_time_V.replace(np.nan,9999).to_csv(os.path.join(outpath,'all_time_V.txt'),sep = ' ')
all_time_chuizhi.replace(np.nan,9999).to_csv(os.path.join(outpath,'all_time_chuizhi.txt'),sep = ' ')

def cal_maidong(df):
    maidong = df - pd.rolling_mean(df,window=12,center=6,min_periods=1)
    return maidong
    
U_maidong = cal_maidong(all_time_U)
V_maidong = cal_maidong(all_time_V)
chuizhi_maidong = cal_maidong(all_time_chuizhi)
#填时间处理的时间范围注意修改！！！
U_maidong['20130628000000':'20130630000000'].replace(np.nan,9999)\
         .to_csv(os.path.join(outpath,datetime.now().strftime('%m-%d-%H-%M-%S') +'U_maidong.txt'),sep = ' ')
V_maidong['20130628000000':'20130630000000'].replace(np.nan,9999)\
         .to_csv(os.path.join(outpath,datetime.now().strftime('%m-%d-%H-%M-%S') +'V_maidong.txt'),sep = ' ')
chuizhi_maidong['20130628000000':'20130630000000'].replace(np.nan,9999)\
         .to_csv(os.path.join(outpath,datetime.now().strftime('%m-%d-%H-%M-%S') +'chuizhi_maidong.txt'),sep = ' ')



