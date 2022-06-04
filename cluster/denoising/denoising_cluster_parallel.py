import os
import sys

# from multiprocess import Pool
import pandas as pd
# from multiprocessing import Pool
# from ast import literal_eval
import itertools
import time
# import spectral_entropy as se
import numpy as np
import toolsets.spectra_operations as so
from molmass import Formula
# import toolsets.tree_denoising as td
# import toolsets.msms_search as ms
# import toolsets.ms2_spectra_plotter as plotter
# import seaborn as sns
# import matplotlib.pyplot as plt
# import toolsets.adduct_calculator as adduct_calc
import yuanyue_code.msp_file as msp_file
import toolsets.mass_to_formula as mtf
import toolsets.denoising_related_functions as de
# %load_ext autoreload
# %autoreload 2

fi = open("hr_msms_nist.MSP")
# fi = open("~/Documents/GitHub/data/NIST/hr_msms_nist.MSP")
# fi = open("yuanyue_code/NIST_demo.msp")
index = int(sys.argv[1])
specs = []
i = 0
for spec in msp_file.read_one_spectrum(fi, include_raw=-1):
    if i <= index:
        try:
            precursormz = float(spec['PrecursorMZ'])
        except ValueError:
            continue
        mol = mtf.MolecularFormula()
        try:
            mol.from_string(spec['Formula'])
        except:
            continue
        specs.append(spec)
        i = i+1
    else:
        break
    
    # if precursormz<=1657.7126:
    #

fi.close()

# import toolsets.test as test
# import multiprocessing as mp
# from multiprocessing import Pool
# Step 1: Init multiprocessing.Pool()
# start = time.time()
# pool = mp.Pool(mp.cpu_count())
# fi = open("/Users/fanzhoukong/Documents/GitHub/data/NIST/hr_msms_nist.MSP")
# fi = open("yuanyue_code/NIST_demo.msp")
# result = []
result = de.find_losses_nist(specs[index])
# for _ in (pool.imap_unordered(de.find_losses_nist, specs)):
#     result.extend(_)
    # result = de.get_unique_list(result)

# results = pool.map_async(de.find_losses_nist, [spec for spec in (msp_file.read_one_spectrum(fi, include_raw=1))])
# fi.close()
# pool.close()
# pool.close()
# pool.join()
# end = time.time()
# print('-fini-')
# print(end-start)
# print(results[:10])
result = de.get_unique_list(result)
result = pd.Series(result)
# input_argv = '1'
outputfilename = 'result'+(sys.argv[1])
print(outputfilename)
print(result)

result.to_csv("result_updated/%s.csv" % outputfilename, index = False)
print("i have things written out")
