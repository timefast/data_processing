# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 16:40:23 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os 
from datetime import datetime

current_path = os.getcwd()
root_sudu = os.path.join(os.path.dirname(current_path),'new_jiaodu/real_data_result')
root_U = os.path.join(os.path.dirname(current_path),'new_maidong/real_data_result')

sudu_df = pd.read_csv(os.path.join(root_sudu,'real_alltime_sudu.txt'),sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
jiaodu_df = pd.read_csv(os.path.join(root_sudu,'real_alltime_new_jiaodu.txt'),sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
          
U = pd.read_csv(os.path.join(root_U,'all_time_U.txt'),sep=' ')\
          .iloc[:,1:].replace(9999,np.nan)
#注意修改实际时间的数量！！！！
U_df = U[:577]

V = pd.read_csv(os.path.join(root_U,'all_time_V.txt'),sep=' ')\
          .iloc[:,1:].replace(9999,np.nan)
#注意修改实际时间的数量！！！！
V_df = V[:577]
#注意sudu_df大小均为：577个时刻*99层
#注意修改时间的范围！！！
rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')
sudu_df.index = rng
jiaodu_df.index = rng
U_df.index = rng
V_df.index = rng

height_index = range(100,6000,60)

gao_index = range(100,2000,60)
sudu_df.columns = height_index
jiaodu_df.columns = height_index
U_df.columns = height_index
V_df.columns = height_index

dti = pd.date_range('20130628000000',periods=577,freq='5min')

select_sudu = sudu_df.loc[dti,gao_index]
select_jiaodu = jiaodu_df.loc[dti,gao_index]
select_U = U_df.loc[dti,gao_index]
select_V = V_df.loc[dti,gao_index]

Cx = np.mean(0.75 * np.asarray(select_sudu.mean()) * np.cos((np.asarray(select_jiaodu.mean()) - 40) * np.pi / 180))
Cy = np.mean(0.75 * np.asarray(select_sudu.mean()) * np.sin((np.asarray(select_jiaodu.mean()) - 40) * np.pi / 180))

def cal_single(u1,u2,v1,v2,cx,cy):
    result =(u2 - cx) * (v1 - cy) - (u1 - cx) * (v2 - cy)
    return result

cal_single_ufunc = np.frompyfunc(cal_single,6,1)
#single_luoxuandu = cal_single_ufunc(select_U.loc['20130628001000'][:-1],select_U.loc['20130628001000'][1:],\
#                                    select_V.loc['20130628001000'][:-1],select_V.loc['20130628001000'][1:],Cx,Cy)
#print single_luoxuandu

luoxuandu = []

for every_time in dti:
    single_luoxuandu = cal_single_ufunc(select_U.loc[every_time][:-1],select_U.loc[every_time][1:],\
                                        select_V.loc[every_time][:-1],select_V.loc[every_time][1:],Cx,Cy)
    luoxuandu.append(single_luoxuandu.astype(np.float).sum(1))

print luoxuandu
    
luoxuandu_df = pd.DataFrame(luoxuandu)
luoxuandu_df.index = dti
luoxuandu_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'xiugai_gao_luoxuandu.txt')