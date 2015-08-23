# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 16:40:23 2015

@author: Administrator
"""

import pandas as pd
import numpy as np

outpath = r'D:\20150803workfile\new_weiwen'

sudu_df = pd.read_csv(r'D:\20150803workfile\new_jiaodu\real_data_result\real_alltime_sudu.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
jiaodu_df = pd.read_csv(r'D:\20150803workfile\new_jiaodu\real_data_result\real_alltime_new_jiaodu.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
          
U = pd.read_csv(r'D:\20150803workfile\new_maidong\real_data_result\all_time_U.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
U_df = U[:577]

V = pd.read_csv(r'D:\20150803workfile\new_maidong\real_data_result\all_time_V.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
V_df = V[:577]
#注意sudu_df大小均为：577个时刻*99层

rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')
sudu_df.index = rng
jiaodu_df.index = rng
U_df.index = rng
V_df.index = rng

height_index = range(100,6000,60)
di_index = range(100,2000,60)
zhong_index = range(2020,4000,60)
gao_index = range(3040,5000,60)
sudu_df.columns = height_index
jiaodu_df.columns = height_index
U_df.columns = height_index
V_df.columns = height_index
print sudu_df.columns
#print jiaodu_df
#print U_df
#print V_df


#select_sudu = sudu_df['20130628001000':'20130628002000']
#select_jiaodu = jiaodu_df['20130628001000':'20130628002000']
#select_U = U_df['20130628001000':'20130628002000']
#select_V = V_df['20130628001000':'20130628002000']

dti = pd.date_range('20130628000000',periods=80,freq='5min')
print dti
#print U_df.loc[dti]
#print select_sudu
#print select_jiaodu
select_sudu = sudu_df.loc[dti,gao_index]
select_jiaodu = jiaodu_df.loc[dti,gao_index]
select_U = U_df.loc[dti,gao_index]
select_V = V_df.loc[dti,gao_index]
print select_sudu
print select_jiaodu
print select_U
print select_V

Cx = 0.75 * np.asarray(select_sudu.mean()) * np.cos((np.asarray(select_jiaodu.mean()) - 40) * np.pi / 180)
Cy = 0.75 * np.asarray(select_sudu.mean()) * np.sin((np.asarray(select_jiaodu.mean()) - 40) * np.pi / 180)
#print select_sudu.mean()
#print select_jiaodu.mean()
#print Cx
#print Cy
#print select_U
#print select_V
#print select_U.loc['20130628001000'][:-1]

def cal_single(u1,u2,v1,v2,cx,cy):
    result =(u2 - cx) * (v1 - cy) - (u1 - cx) * (v2 - cy)
    return result

cal_single_ufunc = np.frompyfunc(cal_single,6,1)
single_luoxuandu = cal_single_ufunc(select_U.loc['20130628001000'][:-1],select_U.loc['20130628001000'][1:],\
                                    select_V.loc['20130628001000'][:-1],select_V.loc['20130628001000'][1:],Cx[:-1],Cy[:-1])
print single_luoxuandu

luoxuandu = []

for every_time in dti:
    single_luoxuandu = cal_single_ufunc(select_U.loc[every_time][:-1],select_U.loc[every_time][1:],\
                                        select_V.loc[every_time][:-1],select_V.loc[every_time][1:],Cx[:-1],Cy[:-1])
    luoxuandu.append(single_luoxuandu.astype(np.float).sum(1))

print luoxuandu
    
luoxuandu_df = pd.DataFrame(luoxuandu)
luoxuandu_df.index = dti
luoxuandu_df.to_csv('test_gao_luoxuandu.txt')