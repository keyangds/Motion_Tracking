# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 10:39:15 2022

@author: xuank
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
import matplotlib.markers as mmark


def getfile():
    import tkinter as Tkinter, tkinter.filedialog as tkFileDialog
    root = Tkinter.Tk()
    root.after(100, root.focus_force)
    root.after(200,root.withdraw)    
    file_path = tkFileDialog.askopenfilename(parent=root,title='Pick a file')    
    return file_path 


def preprocessing(df):
        ## reset each label
        df1 = df.iloc[:,1:]
        for i in range(0,len(df1.iloc[1,:]),3):
            print(i)
            df1.iloc[1,i] = df1.iloc[1,i] +'_'+ df1.iloc[0,i]
            df1.iloc[1,i+1] = df1.iloc[1,i+1] +'_'+ df1.iloc[0,i]
            df1.iloc[1,i+2] = df1.iloc[1,i+2] +'_'+ df1.iloc[0,i]
        df1 = df1.iloc[1:,:]
        df1.columns = df1.iloc[0]
        df1 = df1.iloc[1:,:]
        df1=df1.astype(float)
        
        ## for some low likelihood points, substitue them with the average of t-1 and t+1
        for i in range(2,len(df1.iloc[1,:]),3):
            for j in range(0,len(df1.iloc[:,i])-1):
                if df1.iloc[j,i]<0.8:
                    df1.iloc[j,i-2] = (df1.iloc[j-1,i-2]+df1.iloc[j+1,i-2])/2
                    df1.iloc[j,i-1] = (df1.iloc[j-1,i-1]+df1.iloc[j+1,i-1])/2
            if df1.iloc[-1,i]<0.8:
                df1.iloc[-1,i]=df1.iloc[-2,i]
            
        return df1

def spectral_analysis_x(data):
    ## right_front_paw x coordinate
        f_x, t_x, Sxx_x = signal.spectrogram(data, fs = 40, nperseg = 40, noverlap = 39, mode = 'magnitude')
        
        plt.pcolormesh(t_x,f_x,Sxx_x)
        plt.clim(0,10)  ## set the range of color bar
        plt.colorbar()
        plt.ylabel("Frequency")
        plt.xlabel("Time")

        plt.show() 
        
        average_x = [None]*len(Sxx_x[0])
        s = 0
        count = 0
        for i in range(0, len(Sxx_x[0])):
            for j in range(0,len(Sxx_x)):
                if(Sxx_x[j,i] <= 7.5):
                    count = count + 1
                    s = s + Sxx_x[j,i]    
            average_x[i] = s/count
            s = 0
            count = 0
        
        plt.subplot(1,2,1)
        plt.plot(average_x)
        plt.ylim(0,max(average_x)+1)
        g_x = plt.ginput(1, timeout = -1)
        print(g_x)
        plt.show()
        plt.close("all")
        
        
        start_list = []
        stop_list = []
        start = -1
        stop = 0
        threshold = np.mean(average_x)-1.6*np.std(average_x)
        ##threshold = g_x[0][1]
        for i in range(0,len(average_x)):
            if i == 0:
                if average_x[i] > threshold:
                    start = i
            elif i > 0 and i < len(average_x)-1:
                if average_x[i-1] < threshold and average_x[i+1] > threshold:
                    start = i
                elif average_x[i-1] > threshold and average_x[i+1] < threshold:
                    stop = i
            elif i == len(average_x)-1:
                stop = i
            
            if start >= 0 and stop > start:
                start_list.append(start)
                stop_list.append(stop)
                start = -1
                
        plt.plot(range(0,len(average_x)),average_x,color = 'blue', marker = 'x',mec='r',markevery=start_list, label = "Start")
        plt.plot(range(0,len(average_x)),average_x,color = 'blue', marker = 'o',mec='y',markevery=stop_list, label = "Stop")
        
        '''
        plt.axhline(y = np.mean(average_x), color='k', linestyle='-')
        plt.axhline(y = np.mean(average_x)-np.std(average_x), color='g', linestyle='-')
        plt.axhline(y = np.mean(average_x)-2*np.std(average_x), color='m', linestyle='-')
       
        '''
        plt.legend()
        plt.show()
    
        ## record time points
        record = pd.DataFrame([],columns=['Start','Stop'])
        start = -1
        stop = 0
        for i in range(0,len(average_x)):
            if i == 0:
                if average_x[i] > threshold:
                    start = i
            elif i > 0 and i < len(average_x)-1:
                if average_x[i-1] < threshold and average_x[i+1] > threshold:
                    start = i
                elif average_x[i-1] > threshold and average_x[i+1] < threshold:
                    stop = i
            elif i == len(average_x)-1:
                stop = i
            
            if start >= 0 and stop > start:
                record = record.append({'Start':start, 'Stop': stop}, ignore_index = True)
                start = -1
            
        return record


def spectral_analysis_y(data):
    ## right_front_paw x coordinate
        f_x, t_x, Sxx_y = signal.spectrogram(data, fs = 40, nperseg = 40, noverlap = 39, mode = 'magnitude')
        
        plt.pcolormesh(t_x,f_x,Sxx_y)
        plt.clim(0,10)  ## set the range of color bar
        plt.colorbar()
        plt.ylabel("Frequency")
        plt.xlabel("Time") 
        plt.show() 
        
        average_y = [None]*len(Sxx_y[0])
        s = 0
        count = 0
        for i in range(0, len(Sxx_y[0])):
            for j in range(0,len(Sxx_y)):
                if(Sxx_y[j,i] <= 7.5):
                    count = count + 1
                    s = s + Sxx_y[j,i]
                
            average_y[i] = s/count
            s = 0
            count = 0
            
        plt.subplot(1,2,2)
        plt.plot(average_y)
        plt.ylim(0, max(average_y)+1)
        g_y = plt.ginput(1,timeout = -1)
        print(g_y)
        plt.show()
        plt.close("all")
        
        start_list = []
        stop_list = []
        start = -1
        stop = 0
        ##threshold = np.mean(average_y)-1.6*np.std(average_y)
        threshold = g_y[0][1]
        for i in range(0,len(average_y)):
            if i == 0:
                if average_y[i] > threshold:
                    start = i
            elif i > 0 and i < len(average_y)-1:
                if average_y[i-1] < threshold and average_y[i+1] > threshold:
                    start = i
                elif average_y[i-1] > threshold and average_y[i+1] < threshold:
                    stop = i
            elif i == len(average_y)-1:
                stop = i
            
            if start >= 0 and stop > start:
                start_list.append(start)
                stop_list.append(stop)
                start = -1
                
        plt.plot(range(0,len(average_y)),average_y,color = 'blue', marker = 'x',mec='r',markevery=start_list, label = "Start")
        plt.plot(range(0,len(average_y)),average_y,color = 'blue', marker = 'o',mec='y',markevery=stop_list, label = "Stop")
        '''
        plt.axhline(y = np.mean(average_y), color='k', linestyle='-')
        plt.axhline(y = np.mean(average_y)-np.std(average_y), color='g', linestyle='-')
        plt.axhline(y = np.mean(average_y)-2*np.std(average_y), color='m', linestyle='-')
        '''
        print(np.mean(average_y)-2*np.std(average_y))
        
        plt.legend()
        plt.show()
        
        ## record time points
        record = pd.DataFrame([],columns=['Start','Stop'])
        start = -1
        stop = 0
        for i in range(0,len(average_y)):
            if i == 0:
                if average_y[i] > threshold:
                    start = i
            elif i > 0 and i < len(average_y)-1:
                if average_y[i-1] < threshold and average_y[i+1] > threshold:
                    start = i
                elif average_y[i-1] > threshold and average_y[i+1] < threshold:
                    stop = i
            elif i == len(average_y)-1:
                stop = i
            
            if start >= 0 and stop > start:
                record = record.append({'Start':start, 'Stop': stop}, ignore_index = True)
                start = -1
                
        return record
    
    
def combine_result(r1,r2,l):
    result = pd.DataFrame([],columns=['Start','Stop'])
    i=0
    j=0
    while i < len(r1.iloc[:,0]) and j < len(r2.iloc[:,0]):
        if r1.iloc[i,1] <= r2.iloc[j,0]:
                i = i+1
        elif r2.iloc[j,1] <= r1.iloc[i,0]:
                j = j+1
        # start1 > start2, stop1 < stop2
        elif r1.iloc[i,0] >= r2.iloc[j,0] and r1.iloc[i,1] >= r2.iloc[j,1]:
            result = result.append({'Start':r1.iloc[i,0], 'Stop': r2.iloc[j,1]}, ignore_index = True)
            j = j+1
        
        elif r1.iloc[i,0] >= r2.iloc[j,0] and r1.iloc[i,1] <= r2.iloc[j,1]:
            result = result.append({'Start':r1.iloc[i,0], 'Stop': r1.iloc[i,1]}, ignore_index = True)
            i = i+1
            
        # start1 < start2, stop1 > stop2
        elif r1.iloc[i,0] <= r2.iloc[j,0] and r1.iloc[i,1] <= r2.iloc[j,1]:
            result = result.append({'Start':r2.iloc[j,0], 'Stop': r1.iloc[i,1]}, ignore_index = True)
            i = i+1
            
        elif r1.iloc[i,0] <= r2.iloc[j,0] and r1.iloc[i,1] >= r2.iloc[j,1]:
            result = result.append({'Start':r2.iloc[j,0], 'Stop': r2.iloc[j,1]}, ignore_index = True)
            j = j+1
        
    f_result = pd.DataFrame([],columns=['Start','Stop'])
    for i in range(0,len(result.iloc[:,1])):
        if result.iloc[i,1]-result.iloc[i,0]>=l:
            f_result = f_result.append({'Start':result.iloc[i,0], 'Stop': result.iloc[i,1]}, ignore_index = True)
            
            
    return f_result


## this function helps to select out other useful feature into analysis
def likelihood_test(data,percent):
        count_left_l1 = 0  #for hind left
        
    
        count_left_l2 = 0 
        sum_left_l1 = 0
        sum_left_l2 = 0
        count_right_l1 = 0  #for hind right
        count_right_l2 = 0 
        sum_right_l1 = 0
        sum_right_l2 = 0
        
        for i in data['likelihood_HindLeftPaw']:
            if i < 0.8 and i >= 0.3:
                count_left_l1 = count_left_l1 + 1
                sum_left_l1 + i
            elif i <0.3:
                count_left_l2 = count_left_l2 + 1
                sum_left_l2 + i
        for i in data['likelihood_HindRightPaw']:
            if i < 0.8 and i >= 0.3:
                count_right_l1 = count_right_l1 + 1
                sum_right_l1 + i
            elif i <0.3:
                count_right_l2 = count_right_l2 + 1
                sum_right_l2 + i
                
        count1 = count_left_l1 + count_left_l2
        count2 = count_right_l1 + count_right_l2
        
        sum1 = sum_left_l1 + sum_left_l2
        sum2 = sum_right_l1 + sum_right_l2

        print(count1)
        print(count2)
        
        if (count1/len(data['likelihood_HindLeftPaw'])) > percent and (count2/len(data['likelihood_HindLeftPaw'])) > percent:
            print("No feature qualified")
            return 
        
        if sum_right_l2 > sum_left_l2:
            return 1
        if sum_right_l2 <= sum_left_l2:
            return 0
        
def difference(r1, r2):
    i = 0
    j = 0
    result = pd.DataFrame([],columns=['Start','Stop'])

    while i < len(r2['Start']) and j < len(r1['Start']):
        print(1)
        if r1['Start'][j] == r2['Start'][i]:
            if r1['Stop'][j] == r2['Stop'][i]:
                i = i + 1
                j = j + 1
            elif r1['Stop'][j] < r2['Stop'][i]:
                result = result.append({'Start':r1['Stop'][j], 'Stop': r2['Stop'][i]-1}, ignore_index = True)
                j = j + 1
                        
        elif r1['Start'][j] > r2['Start'][i]:
            if r1['Start'][j] > r2['Stop'][i]:
                i = i + 1
            else:
                result = result.append({'Start':r2['Start'][i], 'Stop': r1['Start'][j]-1}, ignore_index = True)
                if r1['Stop'][j] < r2['Stop'][i]:
                    result = result.append({'Start':r1['Stop'][j], 'Stop': r2['Stop'][i]-1}, ignore_index = True)
                    j = j + 1
                elif r1['Stop'][j] == r2['Stop'][i]:
                    i = i + 1
                    j = j + 1
        print(j, i)
    return result
        
        
#%%

            
    
            
            
        
    