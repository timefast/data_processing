# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 15:09:20 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os 
from datetime import datetime

current_path = os.getcwd()
root_sudu = os.path.join(os.path.dirname(current_path),'new_jiaodu/real_data_result')
root_chuizhi  =  os.path.join(os.path.dirname(current_path),'new_maidong/real_data_result')

sudu_df = pd.read_csv(os.path.join(root_sudu,'real_alltime_sudu.txt'),sep=',')\
          .iloc[:,1:].replace('/////',np.nan)
#注意sudu_df大小均为：577个时刻*99层
chuizhi = pd.read_csv(os.path.join(root_chuizhi,'all_time_chuizhi.txt'),sep=' ')\
          .iloc[:,1:].replace(9999,np.nan)
#注意修改实际的时刻数！！！
chuizhi_df = chuizhi[:577]
##修改时间
rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')
sudu_df.index = rng
chuizhi_df.index = rng
####修改选择的时间！！！
sudu_pieces = [sudu_df.loc['20130628000000'],sudu_df.loc['20130628000500'],sudu_df['20130628001000':'20130628002000'].T]
select_sudu_df = pd.concat(sudu_pieces,axis = 1).T

####修改选择的时间！！！
chuizhi_pieces = [chuizhi_df.loc['20130628000000'],chuizhi_df.loc['20130628000500'],chuizhi_df['20130628001000':'20130628002000'].T]
select_chuizhi_df = pd.concat(chuizhi_pieces,axis = 1).T


temp_df = np.asarray(select_chuizhi_df.mean())
chuizhibianhua =  temp_df[3:] - temp_df[:-3]

pd.DataFrame(chuizhibianhua).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'chuizhibianhua.txt')
select_sudu_df.mean().to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'shuipingpingjun.txt')
select_chuizhi_df.mean().to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'chuizhipingjun.txt')

