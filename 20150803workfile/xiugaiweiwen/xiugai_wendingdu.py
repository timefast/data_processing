# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 17:54:08 2015

@author: Administrator
"""

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
from datetime import datetime

current_path = os.getcwd()
root = os.path.join(os.path.dirname(current_path),'new_jiaodu/real_data_result')
#初始化速度和角度以高度层
height_df=pd.DataFrame({'Height':range(100,6000,60)})
#获得高度矩阵
heightArray = height_df.values + 130
#常量
R = 6371300
fi = 27.79
f = 2 * 7.292 * 10 ** (-5) * np.sin(27.8* np.pi / 180)
#定义计算P函数
def calZ(h):
    #带有float的运算结果也是float,否则全int的结果也为int牺牲了精度
    a =  float(R) * h / (R + h)
    b = (1 + float(h) /R ) **2
    c = 1 - 0.00259 * np.cos(2 * float(fi) * np.pi / 180)
    z = 9.80616 * c * b * a / 9.80665
    return z

calZ_ufunc = np.frompyfunc(calZ,1,1)
Z = calZ_ufunc(heightArray)
#P的type为Object，转换为float
Z = Z.astype(np.float)
#print P
def calP(z):
    temp = np.log10((44331 - z) / 44331) / 0.1903
    p = 1013.255 * 10 ** temp 
    return p

calP_ufunc = np.frompyfunc(calP,1,1)
P = calP_ufunc(Z)
P = P.astype(np.float)

deltaP =  P[:-1] - P[1:]
averP = 0.5 * ( P[:-1] + P[1:] )
C = (averP / deltaP) *( f / 287.05 )  

#print Z
up_aver_P = 0.5 *( P[1:-1] + P[:-2] )
down_aver_P = 0.5 *( P[1:-1] + P[2:] )

def cal_aver_z(x):
    y = 44331 * (1-( x / 1013.255 ) ** 0.1903 )
    return y
    
calaverz_ufunc =  np.frompyfunc(cal_aver_z,1,1)

up_aver_Z = calaverz_ufunc(up_aver_P)
up_aver_Z = up_aver_Z.astype(np.float)
down_aver_Z = calaverz_ufunc(down_aver_P)
down_aver_Z = down_aver_Z.astype(np.float)

jiaodu_df = pd.read_csv(os.path.join(root,'real_alltime_new_jiaodu.txt'),sep=',').replace('/////',np.nan)
sudu_df = pd.read_csv(os.path.join(root,'real_alltime_sudu.txt'),sep=',').replace('/////',np.nan)   
jiaodu = jiaodu_df.T.values
sudu = sudu_df.T.values
#注意jiaodu和sudu大小均为：（1层日期+99层）×577个时刻

#定义位温计算函数，用到数组的元素级别计算
def calWD(c,sudu1,sudu2,jiaodu1,jiaodu2):

    wd = c * float(sudu1) * float(sudu2)* np.sin((float(jiaodu1) - float(jiaodu2)) * np.pi / 180)

    return  wd

calWD_ufunc = np.frompyfunc(calWD,5,1)
WD = calWD_ufunc(C,sudu[1:-1,:],sudu[2:,:],jiaodu[1:-1,:],jiaodu[2:,:])
#print WD 
WDdf = pd.DataFrame(WD)
WDdf.replace(np.nan,9999).to_csv(datetime.now().strftime('%H-%M-%S') +'alltime_wd.txt')
#NumPy中的乘法运算符 * 指示按元素计算 
temp = 1000 * WD[1:,:].astype(np.float) / down_aver_P - 1000 * WD[0:-1,:].astype(np.float) / up_aver_P
delta_z = down_aver_Z - up_aver_Z
result = temp / delta_z
print down_aver_P
print up_aver_P
print down_aver_Z
print up_aver_Z
#print result
result_df = pd.DataFrame(result)
result_df.to_csv(datetime.now().strftime('%H-%M-%S') +'xiugai_alltime_wendingdu.txt')
P_df = pd.DataFrame(P)
P_df.to_csv(datetime.now().strftime('%H-%M-%S') +'P.txt')
Z_df = pd.DataFrame(Z)
Z_df.to_csv(datetime.now().strftime('%H-%M-%S') +'Z.txt')
height_df = pd.DataFrame(heightArray)
height_df.to_csv(datetime.now().strftime('%H-%M-%S') +'height.txt')
#np.savetxt('heightArray.txt',heightArray)


