import toolsets.spectra_operations as so
import pandas as pd
import numpy as np
import multiprocessing as mp
import yuanyue_code.msp_file as msp
import spectral_entropy as se
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import os
import sys
def mute():
    sys.stdout = open(os.devnull, 'w')



def entropy_search_fast(msms, precursormz,library, tolerence= 0.05):
    library_temp = library[(library['PRECURSORMZ'].between(precursormz-(precursormz*10/1E6), precursormz+(precursormz*10/1E6), inclusive=False))]
    entropy = []
    for index, row in library_temp.iterrows():
        entropy_temp = se.similarity(so.convert_string_to_nist(msms), so.convert_string_to_nist(row['msms']), 'entropy',
                                     ms2_da = tolerence, need_clean_spectra = True, need_normalize_result = True)
        entropy.append(entropy_temp)
    index_max = np.argmax(entropy)
    return(entropy[index_max], library_temp.iloc[index_max])




# def entropy_search_old(msms, library, tolerence= 0.05):
#     # for spec in msp.read_one_spectrum(f):
#     #     entropy_temp = se.similarity(so.convert_string_to_nist(msms), spec['spectrum'], 'entropy', ms2_da = tolerence, need_clean_spectra = True, need_normalize_result = True)
#     #     entropy.append(entropy_temp)
#     #     inchi.append(spec['InChIKey'])
#     #     if entropy_temp ==1:
#     #         break
#         #     break
#     #     #     return(entropy_temp, library.iloc[i]['InChIKey'])
#     #     # else:
#     entropy = []
#     for i in range(0, len(library)):
#         entropy_temp=(se.similarity(so.convert_string_to_nist(msms), so.convert_string_to_nist(library.iloc[i]['msms']), 'entropy', ms2_da = tolerence, need_clean_spectra = True, need_normalize_result = True))
#         entropy.append(entropy_temp)
#         #
#
#     index_max = np.argmax(entropy)
#     return(entropy[index_max], index_max)
# def entropy_search_parallel(msms, library, tolerence= 0.05):
#     pool = mp.Pool(mp.cpu_count())
#     entropy = pool.starmap(se.similarity, [(so.convert_string_to_nist(msms), so.convert_string_to_nist(x)'entropy', ms2_da = tolerence, need_clean_spectra = True, need_normalize_result = True) for x in library['msms']])
#
#     pool.close()
#     # pool = mp.Pool(mp.cpu_count())
#     # entropy = [pool.apply(se.similarity, args = (so.convert_string_to_nist(msms),so.convert_string_to_nist(x),'entropy', tolerence, True, True)) for x in library['msms']]
#     # pool.close()
#     index_max = np.argmax(entropy)
#     return(entropy[index_max], library.iloc[index_max]['InChIKey'])
#     # with Pool()as p:
#
# se.similarity()
# def entropy_search_nist(msms, library, tolerance = 0.05):
#     entropy = []
#     for i in range(0, len(library)):
#         entropy_temp=(se.similarity((msms), (library.iloc[i]['msms']), 'entropy', ms2_da = tolerance, need_clean_spectra = True, need_normalize_result = True))
#         if entropy_temp == 1:
#             break
#             return(entropy_temp, library.iloc[i]['InChIKey'])
#         else:
#             entropy.append(entropy_temp)
#     index_max = np.argmax(entropy)
#     return(entropy[index_max], library.iloc[index_max]['InChIKey'])

def exact_lookup(instance, library, typeofmsms='msms', threshold = 0.01):
    entropy = []
    library_subset = library.loc[library['key']==instance['key']]
    for i in range(0, len(library_subset)):
        entropy.append(se.similarity(so.convert_string_to_nist(instance[typeofmsms]), so.convert_string_to_nist(library_subset.iloc[i]['msms']), 'entropy',
                                     ms2_da = threshold, need_clean_spectra = True, need_normalize_result = True))
    index_max = np.argmax(entropy)

    return(entropy[index_max], library_subset.iloc[index_max]['msms'])


# def entropy_match_score_nist(instance, library, typeofmsms='msms'):
#     entropy = []
#     library_subset = library.loc[library['key']==instance['key']]
#     for i in range(0, len(library_subset)):
#         entropy.append(se.similarity((instance[typeofmsms]), (library.iloc[i]['msms']), 'entropy', 0.05, True, True))
#     return(sum(entropy)/len(entropy))

print("i am msms_search!!!!!")



