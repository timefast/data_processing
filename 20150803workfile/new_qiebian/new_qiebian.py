# -*- coding: utf-8 -*-
"""
Created on Mon Aug 03 14:59:37 2015

@author: Administrator
"""

import pandas as pd
import numpy as np
import os

outpath = r'D:\20150803workfile\new_weiwen'

jiaodu_df = pd.read_csv(r'D:\20150803workfile\new_jiaodu\real_data_result\real_alltime_new_jiaodu.txt',sep=',').iloc[:,1:].replace('/////',np.nan)
sudu_df = pd.read_csv(r'D:\20150803workfile\new_jiaodu\real_data_result\real_alltime_sudu.txt',sep=',').iloc[:,1:].replace('/////',np.nan)   
jiaodu = jiaodu_df.T.values.astype(np.float)
sudu = sudu_df.T.values.astype(np.float)
#注意jiaodu和sudu大小均为：99层×577个时刻


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
fengqiebian = cal_fengqiebian_ufunc(jiaodu[:-3,:],jiaodu[3:,:],sudu[:-3,:],sudu[3:,:])

fengqiebian_df = pd.DataFrame(fengqiebian)
fengqiebian_df.to_csv('alltime_chuizhi_qiebian.txt')

shuiping_fengqiebian = cal_fengqiebian_ufunc(jiaodu[:,:-1],jiaodu[:,1:],sudu[:,:-1],sudu[:,1:])
shuiping_fengqiebian_df = pd.DataFrame(shuiping_fengqiebian)
shuiping_fengqiebian_df.to_csv('alltime_shuiping_qiebian.txt')



