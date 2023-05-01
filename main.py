from parser import Searcher

from astropy.io import ascii
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

import time

DATA_DIR = 'data/'
DATA_EXT = '.txt'

table2 = ascii.read('../AT20G/J_MNRAS_434_956/table2.dat', readme='../AT20G/J_MNRAS_434_956/ReadMe').to_pandas()
len_   = table2.shape[0]

files  = [x.name.replace(DATA_EXT, '') for x in sorted(list(Path(DATA_DIR).rglob('*' + DATA_EXT)))]

Seeker = Searcher()

start_  = 1000
ending_ = 2000

for i in range(start_, ending_):
    data = table2.iloc[i]

    if data['AT20G'] not in files:
        intial_time = time.time()
        Seeker.search(data['AT20G'], data['RAh'], data['RAm'],	data['RAs'], data['DE-'], data['DEd'], data['DEm'],	data['DEs'], 2000, DATA_DIR, 'Radio')
        ending_time = time.time()
        print('{0}: {1}. Took time: [{2:.4} s], Completeness [{3:.4}%]'.format(i, data['AT20G'], ending_time - intial_time, (i - start_ + 1) / (ending_ - start_) * 100))
    else:
        print('{0}: {1}. Already Downloaded, Completeness [{2:.4}%]'.format(i, data['AT20G'], (i - start_ + 1) / (ending_ - start_) * 100))