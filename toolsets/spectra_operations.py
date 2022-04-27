#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import yuanyue_code.mass_to_formula as mtf
import re
import pandas as pd
import spectral_entropy as se
import itertools
import numpy as np
import scipy.stats
import warnings
warnings.filterwarnings("ignore")
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def denoising_by_threshold(msms, threshold = 1, need_normalized = False):
    mass_raw, intensity_raw = break_spectra(msms)
    if need_normalized == True:
        intensity_raw = [x/max(intensity_raw) for x in intensity_raw]
    idx=[index for (index, number) in enumerate(intensity_raw) if number > threshold]
    intensity_updated = [intensity_raw[i] for i in idx]
    mass_updated = [mass_raw[i] for i in idx]
    msms_updated = pack_spectra(mass_updated, intensity_updated)
    return(msms_updated)




def break_spectra(spectra):
    split_msms = re.split('\t|\n',spectra)
    intensity = split_msms[1:][::2]
    mass = split_msms[::2]
    mass = [float(item) for item in mass]
    intensity = [float(item) for item in intensity]
    return(mass, intensity)

def pack_spectra(mass, intensity):
    intensity_return = [str(inten) + '\n' for (inten) in (intensity[:-1])]
    intensity_return.append(str(intensity[-1]))
    mass_cali_tab = [str(mas) + '\t' for (mas) in mass]
    list_temp = [None]*(len(mass_cali_tab)+len(intensity_return))
    list_temp[::2] = mass_cali_tab
    list_temp[1::2] = intensity_return
    list_temp = ''.join(list_temp)
    return(list_temp)


def convert_nist_to_string(msms):
    mass = []
    intensity = []
    for n in range(0, len(msms)):
        mass.append(msms[n][0])
        intensity.append(msms[n][1])
    return(pack_spectra(mass,intensity))


def convert_string_to_nist(msms):
    spec_raw = np.array([x.split('\t') for x in msms.split('\n')], dtype=np.float32)
    return(spec_raw)

def normalized_entropy(msms):
    return(scipy.stats.entropy(convert_string_to_nist(msms)[:, 1]))

def entropy_similarity_default(msms1, msms2, typeofmsms='msms', threshold = 0.01):
    # return(se.similarity(convert_string_to_nist(msms1), convert_string_to_nist(msms2), 'entropy', ms2_da = 0.01, need_clean_spectra = True, need_normalize_result = True))
    return(se.similarity(convert_string_to_nist(msms1), convert_string_to_nist(msms2), 'entropy',
                                     ms2_da = threshold, need_clean_spectra = True, need_normalize_result = True))



def average_entropy_calculation(data_temp, typeofmsms = "msms"):
    if len(data_temp)==1:
        # print('you just cannot calculate entropy based on 1 spectrum!!!')
        return(np.NaN)
    else:
        entropy_temp = []
        combinations_object =itertools.combinations(data_temp[typeofmsms], 2)
        for n in combinations_object:
            entropy_temp.append(se.similarity(convert_string_to_nist(n[0]), convert_string_to_nist(n[1]), 'entropy', ms2_da = 0.01, need_clean_spectra = True, need_normalize_result = True))
        return(sum(entropy_temp)/len(entropy_temp))

def average_entropy_dataframe(data_pfp, typeofmsms):
    average_entropy = []
    for i in data_pfp['key'].unique():
        data_temp = data_pfp.loc[data_pfp['key']==i,:]
        entropy_temp = average_entropy_calculation(data_temp, typeofmsms)
        average_entropy.append([entropy_temp]*len(data_temp))
    flat = [x for sublist in average_entropy for x in sublist]
    data_pfp['Average_Entropy']= flat
    return(data_pfp)

def duplicate_handling(data):
    data_final = pd.DataFrame()
    for i in data['key'].unique():
        temp_df = data.loc[data.key == i,:]
        if(len(temp_df) ==1):
            data_final = pd.concat([data_final, temp_df], ignore_index = True, axis = 0)
        else:
            if(temp_df.iloc[0]['Average_Entropy'] >= 0.5):
                data_final = pd.concat([data_final, temp_df[temp_df['intensity'] == temp_df['intensity'].max()]], ignore_index = True, axis = 0)
    return(data_final)




def num_peaks(msms):
    mass, intensity = break_spectra(msms)
    return(len(mass))

from operator import itemgetter
def comparing_spectrum(msms1, msms2):
    if(num_peaks(msms1)<num_peaks(msms2)):
        temp_msms = msms1
        msms1 = msms2
        msms2 = temp_msms
    mass_raw, intensity_raw = so.break_spectra(msms1)
    mass_dr, intensity_dr = so.break_spectra(msms2)
    mass_raw_fl = [float(x) for x in mass_raw]
    mass_dr_fl = [float(x) for x in mass_dr]
    diff_index = [i for i, item in enumerate(mass_raw_fl) if item not in set(mass_dr_fl)]
    mass_diff = list(itemgetter(*diff_index)(mass_raw))
    intensity_diff = list(itemgetter(*diff_index)(intensity_raw))
    rel_intensity_diff = [number / max([float(x) for x in intensity_raw])*100 for number in [float(y) for y in intensity_diff]]
    rel_intensity_kept = [number / max([float(x) for x in intensity_raw])*100 for number in [float(y) for y in intensity_dr]]
    return(mass_diff, intensity_diff, rel_intensity_diff,rel_intensity_kept)





# def explained_intensity(msms1, msms2):
#     if(num_peaks(msms1)<num_peaks(msms2)):
#         temp_msms = msms1
#         msms1 = msms2
#         msms2 = temp_msms
#     mass_raw, intensity_raw = break_spectra(msms1)
#     mass_dr, intensity_dr = break_spectra(msms2)
#     return(sum(intensity_dr)/sum(intensity_raw))

def simple_denoising(instance, typeofmsms = 'msms', ms2_da = 0.01):
    mass, intensity = so.break_spectra(instance[typeofmsms])
    candidates = []
    for mas in mass:
        candidates.append(mtf.nl_to_formula(instance['PRECURSORMZ']-mas, ms2_da, instance['Formula']))
    non_index = [i for i, val in enumerate(candidates) if val != None]
    updated_mass = []
    updated_intensity = []
    for i in non_index:
        updated_mass.append(mass[i])
        updated_intensity.append(intensity[i])
    return(pack_spectra(updated_mass, updated_intensity))





def export_library(data_dup,output_location, typeofmsms='msms'):
    entry = ''
    for index, row in data_dup.iterrows():
        entry = entry + 'NAME: ' + row['NAME'] + '\n'
        entry = entry + 'PRECURSORMZ: ' + str(row['PRECURSORMZ']) + '\n'
        entry = entry + 'InChIKey: ' + row['InChIKey'] + '\n'
        entry = entry + 'Formula: ' + row['Formula'] + '\n'
        entry = entry + 'ExactMass: ' + str(row['ExactMass']) + '\n'
        entry = entry + 'PRECURSORTYPE: ' + row['Adduct'] + '\n'
        entry = entry + 'Collision_enerty: ' + row['Collision_energy'] + '\n'
        # entry = entry + 'RETENTIONTIME: ' + str(row['RETENTIONTIME']) + '\n'
        entry = entry + 'Comment: ' + str(row['Comment']) + '\n'
        entry = entry + 'Num peaks: ' + str(num_peaks(row[typeofmsms])) + '\n'
        entry = entry + row[typeofmsms]
        # entry = entry +str(row['count'])
        entry = entry + '\n'
        entry = entry + '\n'

    #open text file
    text_file = open(output_location, "w",encoding='utf-8')
     
    #write string to file
    text_file.write(entry)
     
    #close file
    text_file.close()
print("i am spectra operation")

