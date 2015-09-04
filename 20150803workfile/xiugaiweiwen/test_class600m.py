# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 17:54:36 2015

@author: Administrator
"""

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
from datetime import datetime

current_path = os.getcwd()
root = os.path.join(os.path.dirname(current_path),r'new_jiaodu/real_data_result')
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

def calP(z):
    temp = np.log10((44331 - z) / 44331) / 0.1903
    p = 1013.255 * 10 ** temp 
    return p

calP_ufunc = np.frompyfunc(calP,1,1)
P = calP_ufunc(Z)
P = P.astype(np.float)

P_df = pd.DataFrame(P)
###P_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'P.txt')
Z_df = pd.DataFrame(Z)
###Z_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'Z.txt')
height_df = pd.DataFrame(heightArray)
###height_df.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'height.txt')


def cal_aver_z(x):
    y = 44331 * (1-( x / 1013.255 ) ** 0.1903 )
    return y
    
calaverz_ufunc =  np.frompyfunc(cal_aver_z,1,1)

jiaodu_df = pd.read_csv(os.path.join(root,'real_alltime_new_jiaodu.txt'),sep=',').replace('/////',np.nan)
sudu_df = pd.read_csv(os.path.join(root,'real_alltime_sudu.txt'),sep=',').replace('/////',np.nan)   

#注意jiaodu和sudu大小均为：（1层日期+99层）×577个时刻

#定义位温计算函数，用到数组的元素级别计算
def calWD(c,sudu1,sudu2,jiaodu1,jiaodu2):

    wd = c * float(sudu1) * float(sudu2)* np.sin((float(jiaodu1) - float(jiaodu2)) * np.pi / 180)

    return  wd

calWD_ufunc = np.frompyfunc(calWD,5,1)

class team_data:
    def __init__(self,sample_number,sample_members):
        self.number = sample_number
        self.members = sample_members
        
    def cal_result(self):
        select_P = P[self.number::self.members]
        deltaP =  select_P[:-1] - select_P[1:]
        averP = 0.5 * ( select_P[:-1] + select_P[1:] )
        C = (averP / deltaP) *( f / 287.05 )  
        up_aver_P = 0.5 *( select_P[1:-1] + select_P[:-2] )
        down_aver_P = 0.5 *( select_P[1:-1] + select_P[2:] )
        
        up_aver_Z = calaverz_ufunc(up_aver_P)
        up_aver_Z = up_aver_Z.astype(np.float)
        down_aver_Z = calaverz_ufunc(down_aver_P)
        down_aver_Z = down_aver_Z.astype(np.float)
        
        jiaodu = jiaodu_df.T.values
        select_jiaodu = jiaodu[(self.number + 1)::self.members,:]
        sudu = sudu_df.T.values
        select_sudu = sudu[(self.number + 1)::self.members,:]
        
        WD = calWD_ufunc(C,select_sudu[:-1,:],select_sudu[1:,:],select_jiaodu[:-1,:],select_jiaodu[1:,:])
        
        WDdf = pd.DataFrame(WD)
        #WDdf.replace(np.nan,9999).T.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') + str(self.number) + 'alltime_wd.txt',sep = ' ')
#NumPy中的乘法运算符 * 指示按元素计算 
        temp = 1000 * WD[1:,:].astype(np.float) / down_aver_P - 1000 * WD[0:-1,:].astype(np.float) / up_aver_P
        delta_z = down_aver_Z - up_aver_Z
        result = temp / delta_z
        
        result_df = pd.DataFrame(result)
        #result_df.replace(np.nan,9999).T.to_csv(datetime.now().strftime('%m-%d-%H-%M-%S')+ str(self.number) +'xiugai_alltime_wendingdu.txt',sep = ' ')
        return [WDdf.T,result_df.T]
        
team0 = team_data(0,10)
[team0_wd,team0_result] = team0.cal_result()
team1 = team_data(1,10)
[team1_wd,team1_result] = team1.cal_result()
team2 = team_data(2,10)
[team2_wd,team2_result] = team2.cal_result()
team3 = team_data(3,10)
[team3_wd,team3_result] = team3.cal_result()
team4 = team_data(4,10)
[team4_wd,team4_result] = team4.cal_result()
team5 = team_data(5,10)
[team5_wd,team5_result] = team5.cal_result()
team6 = team_data(6,10)
[team6_wd,team6_result] = team6.cal_result()
team7 = team_data(7,10)
[team7_wd,team7_result] = team7.cal_result()
team8 = team_data(8,10)
[team8_wd,team8_result] = team8.cal_result()
team9 = team_data(9,10)
[team9_wd,team9_result] = team9.cal_result()

wd_result = pd.DataFrame()
wendingdu_result = pd.DataFrame()

for i in range(8):
    wd_piece = [wd_result,team0_wd.loc[:,i],team1_wd.loc[:,i],team2_wd.loc[:,i],team3_wd.loc[:,i],team4_wd.loc[:,i],\
                          team5_wd.loc[:,i],team6_wd.loc[:,i],team7_wd.loc[:,i],team8_wd.loc[:,i],team9_wd.loc[:,i]]
    wd_result = pd.concat(wd_piece,axis = 1,ignore_index=True)
for i in range(7):
    wendingdu_piece = [wendingdu_result,team0_result.loc[:,i],team1_result.loc[:,i],team2_result.loc[:,i],team3_result.loc[:,i],team4_result.loc[:,i],\
                                        team5_result.loc[:,i],team6_result.loc[:,i],team7_result.loc[:,i],team8_result.loc[:,i],team9_result.loc[:,i]]
    wendingdu_result = pd.concat(wendingdu_piece,axis = 1,ignore_index=True)
i = 8    
wd_piece = [wd_result,team0_wd.loc[:,i],team1_wd.loc[:,i],team2_wd.loc[:,i],team3_wd.loc[:,i],\
                      team4_wd.loc[:,i],team5_wd.loc[:,i],team6_wd.loc[:,i],team7_wd.loc[:,i],team8_wd.loc[:,i]]
wd_result = pd.concat(wd_piece,axis = 1,ignore_index=True)
i = 7
wendingdu_piece = [wendingdu_result,team0_result.loc[:,i],team1_result.loc[:,i],team2_result.loc[:,i],team3_result.loc[:,i],\
                                    team4_result.loc[:,i],team5_result.loc[:,i],team6_result.loc[:,i],team7_result.loc[:,i],team8_result.loc[:,i]]
wendingdu_result = pd.concat(wendingdu_piece,axis = 1,ignore_index=True)

wd_result.replace(np.nan,9999).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'xiugai_alltime_wd600m.txt',sep = ' ')    
wendingdu_result.replace(np.nan,9999).to_csv(datetime.now().strftime('%m-%d-%H-%M-%S') +'xiugai_alltime_wendingdu600m.txt',sep = ' ')

print 'ok'