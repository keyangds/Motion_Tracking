# -*- coding: utf-8 -*-
"""
Created on Thu May 19 18:29:14 2022

@author: xuank
"""
#%%
import os
import matplotlib
import pandas as pd
import numpy as np
#import seaborn as sns
import matplotlib.pyplot as plt
import scipy.io as sio
import mat73
import matplotlib.markers as mmark
from Function import preprocessing, spectral_analysis_x, spectral_analysis_y, combine_result, getfile,likelihood_test, difference
#%%
matplotlib.use('TkAgg')

##path = f\Ebner's Lab\\002-03232021144129-0000DLC_resnet50_Cerebellar_TreadmillApr29shuffle1_900000_filtered.csv"
path = getfile()
df = pd.read_csv(path)
df1 = preprocessing(df)


right_front_paw_data = df1.iloc[:,0:3]
left_front_paw_data = df1.iloc[:,3:6]
right_hind_paw_data = df1.iloc[:,6:9]
left_hind_paw_data = df1.iloc[:,9:12]
nose_data = df1.iloc[:,12:15]
eye_data = df1.iloc[:,15:18]


#%%

## Set threshold for keeping the interval with at least certain length

length = 120
    
#%%
## right_front_paw x coordinate
right_front_record1 = spectral_analysis_x(right_front_paw_data.iloc[:,0])

## right_front_paw y coordinate
right_front_record2 = spectral_analysis_y(right_front_paw_data.iloc[:,1])

result1 = combine_result(right_front_record1,right_front_record2,length)

## left_front_paw x coordinate
left_front_record1 = spectral_analysis_x(left_front_paw_data.iloc[:,0])

## left_front_paw y coordinate
left_front_record2 = spectral_analysis_y(left_front_paw_data.iloc[:,1])

result2 = combine_result(left_front_record1,left_front_record2,length)

## combine result of left and right front paw
result = combine_result(result1,result2,length)


## select hind paw add into analysis
other_feature = likelihood_test(df1)
if other_feature == 1:
    print("left")
    left_hind_record1 = spectral_analysis_x(left_hind_paw_data.iloc[:,1])
    left_hind_record2 = spectral_analysis_y(left_hind_paw_data.iloc[:,1])
    other_result = combine_result(left_hind_record1, left_hind_record2, length)
    
    final_result = combine_result(result,other_result,length)
    
    ## find the interval only front paw moving
    groom = difference(final_result, result)
    
    ## save result with both front and hind
    mdic2 = {"start_stop": np.asarray(final_result.iloc[:,0:2])}
    sio.savemat((path +'final_result.mat'), mdic2, oned_as='column')
    
    mdic3 = {"start_stop": np.asarray(groom.iloc[:,0:2])}
    sio.savemat((path +'groom.mat'), mdic2, oned_as='column')
    
elif other_feature == 0:
    print("right")
    right_hind_record1 = spectral_analysis_x(right_hind_paw_data.iloc[:,1])
    right_hind_record2 = spectral_analysis_y(right_hind_paw_data.iloc[:,1])
    other_result = combine_result(right_hind_record1, right_hind_record2, length)
    
    final_result = combine_result(result,other_result,length)

    ## find the interval only front paw moving
    groom = difference(final_result, result)

    ## save result with both front and hind
    mdic2 = {"start_stop": np.asarray(final_result.iloc[:,0:2])}
    sio.savemat((path +'final_result.mat'), mdic2, oned_as='column')
    
    mdic3 = {"start_stop": np.asarray(groom.iloc[:,0:2])}
    sio.savemat((path +'groom.mat'), mdic2, oned_as='column')

mdic1 = {"start_stop": np.asarray(result.iloc[:,0:2])}
sio.savemat((path +'_front_only_result.mat'), mdic1, oned_as='column')































        

            




