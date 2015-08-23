# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 15:53:20 2015

@author: Administrator
"""

import os
import pandas as pd
import random

root = r'D:\20150803workfile\R\P'

output_path = r'D:\20150803workfile\new_maidong\test_data_maidong_files'

file_list = []
for every_file in os.listdir(root):
    #print every_file
    file_list.append(every_file)
    
#select_files = random.sample(file_list, 3)
select_files = file_list

#select_rows = sorted(random.sample(range(99),3))
select_rows = [0,1,2]

print select_rows
    
for select_file in select_files:
                          
    df=pd.read_csv(os.path.join(root,select_file),skiprows=3,header=None,sep=' ').iloc[select_rows,:4]
    df.to_csv(os.path.join(output_path,select_file))