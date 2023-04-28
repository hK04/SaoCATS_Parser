from parser import Searcher

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

import time

table2 = ascii.read('../AT20G/J_MNRAS_434_956/table2.dat', readme='../AT20G/J_MNRAS_434_956/ReadMe').to_pandas()
len_   = table2.shape[0]

Seeker = Searcher()

start_  = 201
ending_ = 1000

for i in range(start_, ending_):
    data = table2.iloc[i]

    intial_time = time.time()
    Seeker.search(data['AT20G'], data['RAh'], data['RAm'],	data['RAs'], data['DE-'], data['DEd'], data['DEm'],	data['DEs'], 2000, 'data/', 'Radio')
    ending_time = time.time()
    print('{0}: {1}. Took time: [{2:.4} s], Completeness [{3:.4}%]'.format(i, data['AT20G'], ending_time - intial_time, (i - start_ + 1) / (ending_ - start_) * 100))