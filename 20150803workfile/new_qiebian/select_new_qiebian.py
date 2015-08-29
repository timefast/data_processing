# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 14:59:37 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

current_path = os.getcwd()
root_sudu = os.path.join(os.path.dirname(current_path),'new_jiaodu/real_data_result')

jiaodu_df = pd.read_csv(os.path.join(root_sudu,'real_alltime_new_jiaodu.txt'),sep=',').\
                        iloc[:,1:].replace('/////',np.nan)
sudu_df = pd.read_csv(os.path.join(root_sudu,'real_alltime_sudu.txt'),sep=',').\
                      iloc[:,1:].replace('/////',np.nan)

#注意jiaodu和sudu大小均为：99层×577个时刻
print jiaodu_df
#注意修改时间起始！！！！##
rng = pd.date_range(start = '20130628000000', end = '20130630000000', freq='5min')
sudu_df.index = rng
jiaodu_df.index = rng
#注意修改时间窗口！！！
dti = pd.date_range('20130628000000',periods=10,freq='5min')
select_sudu = sudu_df.loc[dti].T.values
select_jiaodu = jiaodu_df.loc[dti].T.values
print select_sudu

def cal_fengqiebian(jiaodu1,jiaodu2,sudu1,sudu2):
    delta = jiaodu2 - jiaodu1
    if np.abs(delta) < 10:
        result = sudu2 - sudu1
    else:
        temp1= sudu1**2
        temp2 = sudu2**2
        temp3 = 2 * sudu1 * sudu2
        temp4 = temp3 *np.cos(delta * np.pi / 180)
        result = (temp1 + temp2 - temp4) ** (0.5)
    print result
                 
    return result
    
cal_fengqiebian_ufunc = np.frompyfunc(cal_fengqiebian,4,1)
fengqiebian = cal_fengqiebian_ufunc(select_jiaodu[:-3,:],select_jiaodu[3:,:],select_sudu[:-3,:],select_sudu[3:,:])

fengqiebian_nofangxiang  = select_sudu[:-3,:] - select_sudu[3:,:]

fengqiebian_df = pd.DataFrame(fengqiebian)
fengqiebian_nofangxiang_df = pd.DataFrame(fengqiebian_nofangxiang)

###注意输出文件名，是alltime或selecttime!!!
fengqiebian_df.T.replace(np.nan,9999).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'selecttime_chuizhi_qiebian.txt',sep = ' ')
fengqiebian_nofangxiang_df.T.replace(np.nan,9999).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'selecttime_chuizhi_qiebian_nofangxiang.txt',sep = ' ')

shuiping_fengqiebian = cal_fengqiebian_ufunc(select_jiaodu[:,:-1],select_jiaodu[:,1:],select_sudu[:,:-1],select_sudu[:,1:])
shuiping_fengqiebian_df = pd.DataFrame(shuiping_fengqiebian)
shuiping_fengqiebian_df.T.replace(np.nan,9999).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'selecttime_shuiping_qiebian.txt',sep = ' ')



