import re
import json
from pathlib import Path

file = 'J125611-054721.txt'
#original header found in all CATS txt outputs
DEFAULT_HEADER = '#----------------------------------------------------------------'

DATA_DIR = 'data/'
DATA_EXT = '.txt'

class CatalogCollector():
    def __init__(self) -> None:
        self.files  = [x for x in sorted(list(Path(DATA_DIR).rglob('*' + DATA_EXT)))]


    def search(self):
        catalogs     = []
        bibs         = []
        lines_       = []
        lines_size   = 0

        for file in self.files:
            with open(file, 'r') as f:
                lines = f.read().split('\n')
                f.close()

            header_index = lines.index(DEFAULT_HEADER)
            lines        = lines[header_index + 1:]
            lines        = [re.sub(' +', ' ', line).split(' ') for line in lines]

            for line in lines:
                if line[2] == ':' and line[3] != 'no':
                    if line[1] not in catalogs and line[3] not in bibs:
                        lines_.append([line[1], [line[3]]])
                        catalogs.append(line[1])
                        bibs.append(line[3])
                        lines_size += 1
                    else:
                        pass
                elif line[2] != ':' and line[1] != ':':
                    if line[1] not in lines_[lines_size - 1][1]:
                        lines_[lines_size - 1][1].append(line[1])
        return lines_

lines = CatalogCollector().search()
print(lines[141])