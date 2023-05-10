from pathlib import Path
from astropy.io import ascii
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

DATA_DIR = 'data/'
DATA_EXT = '.txt'

PLOT_DIR = 'im/'
PLOT_EXT = '.png'

FREQS_MAG = 1000 #plotter should plot frequencies in GHz, while data presented in MHz. So to convert MHz into GHz program diveds frequency by 1000
FLUX_MAG  = 1000 #Flux presented in Jy, to convert it into mJy program multiplies value by 10000

def plotter(fig, ax, name, frequencies, fluxes, catalogs):    
    ax.clear()
    
    catalog_indexes = catalogs.index.to_numpy()
    names = []
    ids_  = []
    for i, ct in enumerate(catalogs):
        if ct not in names:
            names.append(ct)
            ids_.append([catalog_indexes[i]])
        elif ct in names:
            ids_[names.index(ct)].append(catalog_indexes[i])

    ax.clear()
        
    max_y = np.nanmax(fluxes)
    min_y = np.nanmin(fluxes)
    max_x = np.nanmax(frequencies)
    min_x = np.nanmin(frequencies)

    ax.set_yscale('log')
    ax.set_xscale('log')

    ax.set_ylim(min_y/7, max_y*7)
    ax.set_xlim(min_x/7, max_x*7)
    ax.set_ylabel('Flux density, mJy', fontsize = 40)
    ax.set_xlabel(r'$\nu$, GHz', fontsize = 40)


    for i, name_ in enumerate(names):
        ax.scatter(frequencies.loc[ids_[i]], fluxes.loc[ids_[i]], s = 200, label = name_)

    ax.legend(fontsize = 30, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=10)
    ax.set_title(r'Object: {0}. Chart of S($\nu$)'.format(name))

    fig.savefig(PLOT_DIR + str(name) + PLOT_EXT)

files = sorted(list(Path(DATA_DIR).rglob('*' + DATA_EXT)))

objects = pd.Series([path.name.replace(DATA_EXT, '') for path in files])

images  = [x.name.replace(PLOT_EXT, '') for x in sorted(list(Path(PLOT_DIR).rglob('*' + PLOT_EXT)))]

fig, ax = plt.subplots(figsize = (40, 40))
plt.rcParams.update({'font.size' : 40})

start_ = 0
ending_ = len(files)

counter_of_broken = 0
broken_files      = []

if __name__ == "__main__":
    for i, file in enumerate(files[start_:ending_]):

        freqs = []
        flux  = []

        ERROR_DATA = 0
        ERROR_PLOT = 0

        try:
            data  = ascii.read(file).to_pandas()
            freqs = data['col11'][data['col11'].astype(str).str.isdigit() == True].astype('float64') / FREQS_MAG
            flux  = data['col12'][data['col11'].astype(str).str.isdigit() == True].astype('float64') * FLUX_MAG
            catalogs = data['col1'][data['col11'].astype(str).str.isdigit() == True]
            #print(pd.DataFrame(data = np.array([freqs, flux]).T, columns=['freqs', 'flux']))
        except:
            ERROR_DATA = 1
        
        if not ERROR_DATA:
            try:
                if str(objects[i]) not in images:
                    plotter(fig, ax, objects[i], freqs, flux, catalogs)
                else:
                    pass
            except:
                ERROR_PLOT = 1
            
        if ERROR_PLOT:
            print('{0}: {1}, PLOT ERROR'.format(i, objects[i]))
        if ERROR_DATA:
            print('{0}: {1}, DATA ERROR'.format(i, objects[i]))
        if ERROR_DATA or ERROR_PLOT:
            counter_of_broken += 1
            broken_files.append(objects[i])
        else:
            print('{0}: {1}, Completeness [{2:.4}%], Plot_shape: {3}'.format(i, objects[i], (i - start_ + 1) / (ending_ - start_) * 100, len(freqs)))
        
    print(counter_of_broken)
    print(broken_files)