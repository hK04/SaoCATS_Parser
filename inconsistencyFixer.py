inconsistencies = ['PKS ', 'PCNT G', '_G', ' G', 'NRAO ', 'NAIC5G', '3CR   ', '3C ', 'MSLGC', 'SMC ', 'NGC ']
fixes = ['PKS', 'PCNTG', 'G', 'G', 'NRAO', 'NAIC5G ', '3CR', '3C', 'MSLGC ', 'SMC', 'NGC']

def fix_str(str):
    for i, inconsitency in enumerate(inconsistencies):
        str = str.replace(inconsitency, fixes[i])
    return str

def fix_text(file):
    with open(file, 'r') as f:
        text = f.read()
        f.close()

    for i, inconsitency in enumerate(inconsistencies):
        text = text.replace(inconsitency, fixes[i])

    with open(file, 'w') as f:
        f.write(text)
        f.close()

if __name__ == "__main__":
    DATA_DIR = 'data/'
    DATA_EXT = '.txt'
    from pathlib import Path
    files = sorted(list(Path(DATA_DIR).rglob('*' + DATA_EXT)))

    for file in files:
        fix_text(file)