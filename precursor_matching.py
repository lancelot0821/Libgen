import pandas as pd
import itertools
import numpy as np
def readin_MSDIAL(file):
    df = pd.read_csv(file, sep = '\t', header=[4])
    return(df)
def precursor_matching(df, sample_list, mzmmu, adducts, comments, threshold = 0.3):
    mz_mmu = mzmmu
    data_raw = pd.DataFrame(columns = ['NAME','key','PRECURSORMZ','InChIKey','Formula',
                       'ExactMass','adduct','Spectrum_type','RETENTIONTIME','Average_mz',
                       'Comment', 'Alignment_ID','Num_Peaks','msms','count','intensity','mix_label'])
    ms2df = df.loc[(df['MS/MS assigned']) & (df['Fill %'] < threshold)]
    # parameters
    # this is already matching the spectrum in the same data file
    spectrum_type = 'MS2'
    # adducts = ['[M+H]+', '[M+NH4]+', '[M+Na]+']
    # comments = ' EAD spectrum'
    for mix in ms2df.columns[32:-2]:
        for index, df_row in ms2df[ms2df['Spectrum reference file name'] == mix].iterrows():
            msms = df_row['MS/MS spectrum'].replace(' ', '\n').replace(':', '\t')
            nlines = msms.count('\n')+1
            mz_lower = df_row['Average Mz'] - mz_mmu * 0.001
            mz_upper = df_row['Average Mz'] + mz_mmu * 0.001
            for index, ls_row in sample_list[sample_list['Mix label'] == mix].iterrows():
                for adduct in adducts:
                    if ls_row[adduct] > mz_lower  and ls_row[adduct] < mz_upper:
                        data_raw = data_raw.append({
                                                    'NAME':ls_row['Name'],
                                                   'key':ls_row['InChiKey']+adduct,
                                                   'PRECURSORMZ':(float(ls_row[adduct])),
                                                   'InChIKey':ls_row['InChiKey'],
                                                    'Formula':ls_row['Formula'],
                                                    'ExactMass':(float(ls_row['Exact Mass'])),
                                                    'adduct':adduct,
                                                    'Spectrum_type':spectrum_type,
                                                    'RETENTIONTIME':(float(df_row['Average Rt(min)'])),
                                                    'Average_mz':(float(df_row['Average Mz'])),
                                                    'Comment':str(df_row['Alignment ID']) + comments + ' intensity ' + str(df_row[mix]),
                                                    'Alignment_ID':(df_row['Alignment ID']),
                                                    'Num_Peaks':int(nlines),
                                                    'msms':msms,
                                                    'intensity':(df_row[mix]),
                                                    'mix_label':mix,
                                                   'count':str('na')}, ignore_index=True)
    occ = data_raw.key.value_counts(normalize=False, sort = False)


    data_raw_count = pd.DataFrame()
    for i in range(len(occ)):
        temp_df = data_raw.loc[data_raw.key == occ.index[i],:]
        temp_df['count'] = temp_df['count'].replace(['na'], int(occ[i]))
        data_raw_count=pd.concat([data_raw_count, temp_df], ignore_index = True, axis = 0)
    data_raw_count['row_num'] = np.arange(len(data_raw_count))
    data_raw_count.round({'PRECURSORMZ':6})
    data_raw_count['PRECURSORMZ']=pd.to_numeric(data_raw_count['PRECURSORMZ'])
    data_raw_count['ExactMass']=pd.to_numeric(data_raw_count['ExactMass'])
    data_raw_count['Average_mz']=pd.to_numeric(data_raw_count['Average_mz'])
    data_raw_count['intensity']=pd.to_numeric(data_raw_count['intensity'])
    data_raw_count['Num_Peaks']=pd.to_numeric(data_raw_count['Num_Peaks'])
    data_raw_count['RETENTIONTIME']=pd.to_numeric(data_raw_count['RETENTIONTIME'])
    return(data_raw_count)

print("I am precursor matching!")