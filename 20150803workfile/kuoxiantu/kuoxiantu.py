# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 15:09:20 2015

@author: Administrator
"""

import pandas as pd
import numpy as np

outpath = r'D:\20150803workfile\new_weiwen'

sudu_df = pd.read_csv(r'D:\20150803workfile\new_jiaodu\real_data_result\real_alltime_sudu.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
#注意sudu_df大小均为：577个时刻*99层
chuizhi = pd.read_csv(r'D:\20150803workfile\new_maidong\real_data_result\all_time_chuizhi.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
chuizhi_df = chuizhi[:577]

rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')
sudu_df.index = rng
chuizhi_df.index = rng

sudu_pieces = [sudu_df.loc['20130628000000'],sudu_df.loc['20130628000500'],sudu_df['20130628001000':'20130628002000'].T]
select_sudu_df = pd.concat(sudu_pieces,axis = 1).T
#print select_sudu_df.mean()

chuizhi_pieces = [chuizhi_df.loc['20130628000000'],chuizhi_df.loc['20130628000500'],chuizhi_df['20130628001000':'20130628002000'].T]
select_chuizhi_df = pd.concat(chuizhi_pieces,axis = 1).T
#print select_chuizhi_df.mean()

temp_df = np.asarray(select_chuizhi_df.mean())
chuizhibianhua =  temp_df[3:] - temp_df[:-3]
np.savetxt('chuizhibianhu.txt',chuizhibianhua)
np.savetxt('shuipingpingjun.txt',select_sudu_df.mean())
np.savetxt('chuizhipingjun.txt',select_chuizhi_df.mean())
