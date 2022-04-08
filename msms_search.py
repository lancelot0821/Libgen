import spectra_operations as so
import pandas as pd
import numpy as np
import spectral_entropy as se
def entropy_search(msms, library):
    entropy = []
    for i in range(0, len(library)):
        entropy_temp=(se.similarity(so.convert_string_to_nist(msms), so.convert_string_to_nist(library.iloc[i]['msms']), 'entropy', ms2_da = 0.05, need_clean_spectra = True, need_normalize_result = True))
        if entropy_temp ==1:
            break
            return(entropy_temp, i)
        else:
            entropy.append(entropy_temp)
    index_max = np.argmax(entropy)
    return(entropy[index_max], index_max)
def entropy_match_score(instance, library, typeofmsms='msms'):
    entropy = []
    library_subset = library.loc[library['key_all']==instance['key_all']]
    for i in range(0, len(library_subset)):
        entropy.append(se.similarity(so.convert_string_to_nist(instance[typeofmsms]), so.convert_string_to_nist(library.iloc[i]['msms']), 'entropy', ms2_da = 0.05, need_clean_spectra = True, need_normalize_result = True))
    return(sum(entropy)/len(entropy))

print("i am msms_search!")



