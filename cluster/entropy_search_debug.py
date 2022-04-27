import os
import sys

import pandas as pd
from ast import literal_eval
import os
import itertools
import time
import spectral_entropy as se

import numpy as np
import toolsets.spectra_operations as so
import numpy as np
import yuanyue_code.msp_file as msp
# import scipy.stats
import toolsets.tree_denoising as td
import toolsets.msms_search as ms
# import toolsets.ms2_spectra_plotter as plotter
# import setup
import seaborn as sns
import matplotlib as plt
data = pd.read_csv(sys.argv[1])
library = pd.read_csv(sys.argv[2])
f = open(sys.argv[3])
tolerance = float(sys.argv[4])
specs = []
for spec in msp.read_one_spectrum(f):
    specs.append(spec)
f.close()
for appendix in ['msms','msms_dfrag','msms_d1']:
    globals()['entropy_%s' % appendix]=[]
    globals()['matched_inchi_%s'% appendix]=[]
    globals()['matched_eva_%s' % appendix]=[]

for index, row in data.iloc[0:2].iterrows():
    for appendix in ['msms','msms_dfrag','msms_d1']:
        entropy_temp, index = ms.entropy_search(row[appendix], specs, tolerance)
        globals()['entropy_%s' % appendix].append(entropy_temp)
        globals()['matched_inchi_%s'% appendix].append(library.iloc[index]['InChIKey'])
        if row['InChIKey']==library.iloc[index]['InChIKey']:
            globals()['matched_eva_%s' % appendix].append(True)
        else:
            globals()['matched_eva_%s' % appendix].append(False)

for appendix in ['msms','msms_dfrag','msms_d1']:
    data['entropy_'+appendix]=globals()['entropy_%s' % appendix]
    data['matched_inchi_'+appendix] = globals()['matched_inchi_%s'% appendix]
    data['mached_eva_'+appendix]=globals()['matched_eva_%s' % appendix]
data.to_csv(sys.argv[5])
