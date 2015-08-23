# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 08:16:03 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

current_path = os.getcwd()
root_sudu = os.path.join(os.path.dirname(current_path),'new_jiaodu/real_data_result')

sudu_df = pd.read_csv(os.path.join(root_sudu,'real_alltime_sudu.txt'),sep=',')\
          .iloc[:,1:].replace('/////',np.nan).T   
#注意sudu_df大小均为：99层×577个时刻

height_index = range(100,6000,60)
di_index = range(100,2000,60)
zhong_index = range(2020,4000,60)
gao_index = range(4000,6000,60)

sudu_df.index = height_index

#sudu的index为高度，第一列也为高度，99层×（577时刻+1高度列）

[di_sudu,di_gaodu] = [sudu_df.loc[di_index,:].max(),sudu_df.loc[di_index,:].idxmax()]
pd.concat([di_sudu,di_gaodu],ignore_index=True,axis=1).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'di.txt')

[zhong_sudu,zhong_gaodu] = [sudu_df.loc[zhong_index,:].max(),sudu_df.loc[zhong_index,:].idxmax()]
pd.concat([zhong_sudu,zhong_gaodu],ignore_index=True,axis=1).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'zhong.txt')

[gao_sudu,gao_gaodu] = [sudu_df.loc[gao_index,:].max(),sudu_df.loc[gao_index,:].idxmax()]
pd.concat([gao_sudu,gao_gaodu],ignore_index=True,axis=1).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'gao.txt')

jiliuzhishu = np.asarray(zhong_sudu) / (np.asarray(zhong_gaodu) - np.asarray(di_gaodu))

#注意修改时间范围
rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')
jiliuzhishu_df = pd.DataFrame(jiliuzhishu)
jiliuzhishu_df.index = rng
jiliuzhishu_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'jiliuzhishu.txt')

sudu12 = sudu_df - 12
mask_sudu12 = sudu12.mask(sudu12 < 0)
[sudu_12,gaodu_12] = [mask_sudu12.min(),mask_sudu12.idxmin()]
pd.concat([sudu_12,gaodu_12],ignore_index=True,axis=1).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'12_height.txt')
qiangduzhishu = np.asarray(di_sudu) / (np.asarray(gaodu_12) + 130)
qiangduzhishu_df = pd.DataFrame(qiangduzhishu)
qiangduzhishu_df.index = rng

qiangduzhishu_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'qiangduzhishu.txt')

half_di_index = range(100,3000,60)
half_gao_index = range(3040,6000,60)
half_di_sudu12 = sudu_df.loc[half_di_index,:]-12 
mask_half_di_sudu12 = half_di_sudu12.mask(half_di_sudu12 < 0)
[half_di_sudu,half_di_gaodu] = [mask_half_di_sudu12.min(),mask_half_di_sudu12.idxmin()]

half_gao_sudu20 = sudu_df.loc[half_gao_index,:]-20 
mask_half_gao_sudu20 = half_gao_sudu20.mask(half_gao_sudu20 < 0)
[half_gao_sudu,half_gao_gaodu] = [mask_half_gao_sudu20.min(),mask_half_gao_sudu20.idxmin()]

pd.concat([half_di_sudu,half_di_gaodu],ignore_index=True,axis=1).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'half_di.txt')
pd.concat([half_gao_sudu,half_gao_gaodu],ignore_index=True,axis=1).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'half_gao.txt')
di_jiliuzhishu =  12 / (np.asarray(half_di_gaodu) + 130)
gao_jiliuzhishu = 20 / (np.asarray(half_gao_gaodu) + 130)
di_jiliuzhishu_df = pd.DataFrame(di_jiliuzhishu)
gao_jiliuzhishu_df = pd.DataFrame(gao_jiliuzhishu)
di_jiliuzhishu_df.index = rng
gao_jiliuzhishu_df.index = rng
di_jiliuzhishu_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'di_jiliuzhishu.txt')
gao_jiliuzhishu_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'gao_jiliuzhishu.txt')

