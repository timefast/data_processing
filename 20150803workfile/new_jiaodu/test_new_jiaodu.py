# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 07:47:55 2015

@author: Administrator
"""

import os
import pandas as pd
import numpy as np

root = r'D:\20150803workfile\new_maidong\test_data_maidong_files'
outpath = r'D:\20150803workfile\new_jiaodu\test_data_result'

all_jiaodu = pd.DataFrame()

all_time = []

#定义计算函数，用到数组的元素级别计算
def get_new_jiaodu(jiaodu):
    
    if jiaodu < 270:
        new_jiaodu = 270 - float(jiaodu)
    else:
        new_jiaodu = 360 + 270 - float(jiaodu)
        
    return new_jiaodu

for every_file in os.listdir(root):
#每个文件取一列
    df_jiaodu=pd.read_csv(os.path.join(root,every_file),sep=',').iloc[:,2].replace('/////',np.nan)
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
   
#解析文件名中所包含的日期并转换为datatime格式    
    time_index = pd.to_datetime(every_file.split('_')[4])
    all_time.append(time_index)
        
#把time作为index
all_jiaodu.index = all_time
all_jiaodu.to_csv(os.path.join(outpath,'test_new_jiaodu.txt'))