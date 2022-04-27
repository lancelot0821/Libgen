import os

import pandas as pd

from ast import literal_eval
import os
import itertools
import time
import sys
import shutil
import warnings
warnings.filterwarnings("ignore")
import spectral_entropy as se
import numpy as np
import toolsets.spectra_operations as so
import numpy as np
import toolsets.tree_denoising as td
data_mona_common =pd.read_csv("MONA_common_with_nist.csv")



msms_d = []
explained_intensity = []
for index, row in data_mona_common.iterrows():
    msms_d.append(td.readin_denoised_msms(row, 'MONA_common','MONA_common','50ppm','20ppm'))
    explained_intensity.append(td.readin_denoised_something('explainedIntensity',row, 'MONA_common','MONA_common','50ppm','20ppm'))
data_mona_common['msms_dfrag']=msms_d
data_mona_common['explained_intensity']=explained_intensity
data_mona_common.to_csv("data_mona_common_updated.csv", index = False)