#!/usr/bin/env python
# coding: utf-8

# In[10]:


from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import toolsets.spectra_operations as so
def mass_fitting(mass_measured, lm_temp):
    mass_cali = lm_temp.predict(np.array(mass_measured, dtype = float ).reshape(-1,1)) 
    mass_cali = [round(num, 6) for num in mass_cali]
#     mass_cali = [str(integer) for integer in mass_cali]
    return(mass_cali)
    

def fit_model(measured, actual):
    if(len(measured)>1):
        x = measured.values.reshape(-1,1)
        y = actual.values
        lm = LinearRegression().fit(x,y)
        return(lm)
    else:
        x = np.array([1,2,3]).reshape(-1,1)
        y = np.array([1,2,3])
        lm = LinearRegression().fit(x,y)
        return(lm)
    
def mass_recalibrate(lm, msms):
    mass, intensity = so.break_spectra(msms)
    mass_recali = mass_fitting(mass, lm)
    msms_recali = so.pack_spectra(mass_recali, intensity)
    return(msms_recali)
        

def data_recalibrate(data):
    data_recalibrated = pd.DataFrame()
    for i in data['mix_label'].unique():
        data_temp = data.loc[data['mix_label']==i]
        x_temp = data_temp['Average_mz']
        y_temp = data_temp['PRECURSORMZ']
        lm_temp = fit_model(x_temp, y_temp)
        msms_recalibrated = []
        for n in range(len(data_temp)):
            msms_recalibrated.append(mass_recalibrate(lm_temp, data_temp.iloc[n]['msms']))
        data_temp['mass_recalibrated']=msms_recalibrated
        data_recalibrated = pd.concat([data_recalibrated, data_temp], ignore_index = True, axis = 0)
    return(data_recalibrated)


# # this 'data' has to have the 'mass_recalibrated' column!!!!
# def error_analysis(data_recalibrated, mix_label):
#     msms_measured_all = []
#     msms_cali_all =[]
#     data_temp = data_recalibrated[data_recalibrated['mix_label'] == mix_label]
#     for i in range(len(data_temp)):
#         split_msms =re.split('\t|\n',data_temp['msms'].iloc[i]) 
#         msms_measured = split_msms[::2]
#         split_msms_re =re.split('\t|\n',data_temp['mass_recalibrated'].iloc[i]) 
#         msms_cali = split_msms_re[::2]
#         msms_measured_num = np.array(msms_measured, dtype = float)
#         msms_cali_num = np.array(msms_cali, dtype = float)
#         msms_measured_all=np.concatenate((msms_measured_all,msms_measured_num), axis = None)
#         msms_cali_all=np.concatenate((msms_cali_all, msms_cali_num), axis = None)
                
#     return(msms_measured_all,msms_cali_all)


# In[2]:


print("I am mass recalibration, usage: mass_recalibrate(measured MZ(list), PRECURSORMZ (list), msms (single_msms)!")

