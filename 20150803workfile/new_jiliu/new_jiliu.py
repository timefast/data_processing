# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 08:16:03 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

outpath = r'D:\20150803workfile\new_weiwen'

sudu_df = pd.read_csv(r'D:\20150803workfile\new_jiaodu\real_data_result\real_alltime_sudu.txt',sep=',')\
          .iloc[:,1:].replace('/////',np.nan).T   
#注意sudu_df大小均为：99层×577个时刻

height_index = range(100,6000,60)
di_index = range(100,2000,60)
zhong_index = range(2020,4000,60)
gao_index = range(4000,6000,60)

sudu_df.index = height_index
#sudu_ready = sudu_df.reset_index(drop=False)
#sudu_ready.index = height_index
#sudu的index为高度，第一列也为高度，99层×（577时刻+1高度列）

#print sudu_ready['index']
#print sudu_ready.loc[di_index,:]
[di_sudu,di_gaodu] = [sudu_df.loc[di_index,:].max(),sudu_df.loc[di_index,:].idxmax()]
pd.concat([di_sudu,di_gaodu],ignore_index=True,axis=1).to_csv('di.txt')

[zhong_sudu,zhong_gaodu] = [sudu_df.loc[zhong_index,:].max(),sudu_df.loc[zhong_index,:].idxmax()]
pd.concat([zhong_sudu,zhong_gaodu],ignore_index=True,axis=1).to_csv('zhong.txt')

[gao_sudu,gao_gaodu] = [sudu_df.loc[gao_index,:].max(),sudu_df.loc[gao_index,:].idxmax()]
pd.concat([gao_sudu,gao_gaodu],ignore_index=True,axis=1).to_csv('gao.txt')
#print [gao_sudu,gao_gaodu]
jiliuzhishu = np.asarray(zhong_sudu) / (np.asarray(zhong_gaodu) - np.asarray(di_gaodu))
np.savetxt('jiliuzhishu.txt',jiliuzhishu)
#print jiliuzhishu
#jiliuzhishu.to_csv('zhishu.txt')
sudu12 = sudu_df - 12
abssudu12 = sudu12.abs()
[sudu_12,gaodu_12] = [abssudu12.min(),abssudu12.idxmin()]
pd.concat([sudu_12,gaodu_12],ignore_index=True,axis=1).to_csv('12_height.txt')
qiangduzhishu = np.asarray(di_sudu) / (np.asarray(gaodu_12) + 130)
np.savetxt('qiangduzhishu.txt',qiangduzhishu)

half_di_index = range(100,3000,60)
half_gao_index = range(3040,6000,60)
[half_di_sudu,half_di_gaodu] = [(sudu_df.loc[half_di_index,:]-12).abs().min(),(sudu_df.loc[half_di_index,:]-12).abs().idxmin()]
[half_gao_sudu,half_gao_gaodu] = [(sudu_df.loc[half_gao_index,:]-20).abs().min(),(sudu_df.loc[half_gao_index,:]-20).abs().idxmin()]
pd.concat([half_di_sudu,half_di_gaodu],ignore_index=True,axis=1).to_csv('half_di.txt')
pd.concat([half_gao_sudu,half_gao_gaodu],ignore_index=True,axis=1).to_csv('half_gao.txt')
di_jiliuzhishu =  12 / (np.asarray(half_di_gaodu) + 130)
gao_jiliuzhishu = 20 / (np.asarray(half_gao_gaodu) + 130)
np.savetxt('di_jiliuzhishu.txt',di_jiliuzhishu)
np.savetxt('gao_jiliuzhishu.txt',gao_jiliuzhishu)
