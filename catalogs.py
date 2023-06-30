import re
import json
import os
import requests #usage instead of pointless nasa_ads library from astroquery 
from pathlib import Path
from bs4 import BeautifulSoup
from astroquery.simbad import Simbad
from astroquery import nasa_ads as na
from astroquery.exceptions import TableParseError
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlencode, quote_plus 

#original header found in all CATS txt outputs
DEFAULT_HEADER = '#----------------------------------------------------------------'

DATA_DIR = 'data/'
DATA_EXT = '.txt'

NASA_ADS_API_SEARCH    = 'https://api.adsabs.harvard.edu/v1/search/query?'
NASA__ADS_API_DOWNLOAD = 'https://ui.adsabs.harvard.edu/link_gateway/'
NASA_ADS_TOKEN         = 'DlUEZZV6jSJW5PopnQUopbObbJGNmlOpYfPijcMT'

ARTICLES_DIR = 'articles/'

def request(url, headers = ''):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session.get(url, headers=headers)

class CatalogCollector():
    def __init__(self) -> None:
        self.files  = [x for x in sorted(list(Path(DATA_DIR).rglob('*' + DATA_EXT)))]

    def searchForArticlesBibs(self) -> list:
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

    def searchForDoi(self, bib : str) -> dict:
        doi   = ''
        title = ''

        try: 
            result_table = Simbad.query_bibcode(bib)
        except TableParseError:
            print('Simbad exception occurred. Proceed with search manually')
            
            return {'doi': doi, 'title': title}
        
        try:
            BibReply = re.sub(' +', ' ', str(result_table)).split(' ')
            index_   = BibReply.index('DOI')
            search   = BibReply[index_ + 1].split('\\n')[0]

            doi = search
        except:
            pass

        try:
            BibReply = re.sub(' +', ' ', str(result_table)).split('Flags: ')[0].split('\\n')
            while BibReply[-1] == '':
                BibReply = BibReply[:-1]
            search = BibReply[-1]

            title = search
        except:
            pass

        return {'doi': doi, 'title': title}

    def searchForMetaByDoi(self, doi : str) -> dict:
        if doi != '':
            encoded_query = urlencode({"q": "doi:{0}".format(doi),
                            "fl": "abstract, title, bibcode",
                            "rows" : 1})
            
            results = requests.get(NASA_ADS_API_SEARCH + '{}'.format(encoded_query), \
                        headers={'Authorization': 'Bearer ' + NASA_ADS_TOKEN})
            #data in form of array of dicts {title : <>, abstract : <>}
            try:
                return json.loads(results.text)['response']['docs']
            except KeyError:
                return {}
        else:
            return {}
        
    
    def searchForMetaByTitle(self, title : str) -> dict:
        if title != '':
            encoded_query = urlencode({"q": "{0}".format(title),
                            "fl": "abstract, title, bibcode",
                            "rows" : 3})
            
            results = requests.get(NASA_ADS_API_SEARCH + '{}'.format(encoded_query), \
                        headers={'Authorization': 'Bearer ' + NASA_ADS_TOKEN})
            #data in form of array of dicts {title : <>, abstract : <>}
            try:
                return json.loads(results.text)['response']['docs']
            except KeyError:
                return {}

        else:
            return {}
    
    def downloadPdfByBib(self, bib : str, dir : str, filename : str):
        try:
            response_1 = requests.get(NASA__ADS_API_DOWNLOAD + bib + '/EPRINT_PDF')
        except requests.exceptions.ConnectionError:
            print('{0} is not available'.format(NASA__ADS_API_DOWNLOAD + bib + '/EPRINT_PDF'))
            response_1 = ''

        try:
            response_2 = requests.get(NASA__ADS_API_DOWNLOAD + bib + '/PUB_PDF') 
        except requests.exceptions.ConnectionError:
            print('{0} is not available'.format(NASA__ADS_API_DOWNLOAD + bib + '/PUB_PDF'))
            response_2 = ''

        if response_1 != '' and response_2 != '':
            soup_1 = BeautifulSoup(response_1.text, 'html.parser')
            soup_2 = BeautifulSoup(response_2.text, 'html.parser')
        elif response_1 != '':
            soup_1 = BeautifulSoup(response_1.text, 'html.parser')
            soup_2 = soup_1 
        elif response_2 != '':
            soup_2 = BeautifulSoup(response_2.text, 'html.parser')
            soup_1 = soup_2
        else:
            return 

        if soup_1.title == None:
            response = response_1
        elif soup_2.title == None:
            response = response_2
        elif soup_2.title.text == 'ShieldSquare Captcha':
            print('Captcha Protection, Download form {0} manually'.format(NASA__ADS_API_DOWNLOAD + bib + '/PUB_PDF'))

            return
        else:
            return 

        try:
            with open(dir + '/' + filename + '.pdf', 'wb') as f:
                f.write(response.content)
                f.close()
        except FileNotFoundError:
            os.mkdir(dir)

            with open(dir + '/' + filename + '.pdf', 'wb') as f:
                f.write(response.content)
                f.close()
        except UnboundLocalError:
            print('No article found')

            return 
        
        return response.text

if __name__ == '__main__':
    lines = CatalogCollector().searchForArticlesBibs()
    for line in lines:
        dir_name = str(line[0]) + '/'
        for bib in line[1]:
            dict   = CatalogCollector().searchForDoi(bib)

            if dict['doi']   != '':
                meta_1 = CatalogCollector().searchForMetaByDoi(dict['doi'])
            else:
                meta_1 = []

            if dict['title'] != '':
                meta_2 = CatalogCollector().searchForMetaByTitle(dict['title'])
            else:
                meta_2 = []

            if meta_1 != {}:
                for meta in meta_1:
                    print(meta['bibcode'])
                    try:
                        name = ARTICLES_DIR +  dir_name + '/' + meta['bibcode'] + '.pdf'
                        with open(name.replace('//', '/') , 'r') as f:
                            f.close()
                    except FileNotFoundError:
                        CatalogCollector().downloadPdfByBib(meta['bibcode'], ARTICLES_DIR +  dir_name, meta['bibcode'])
            if meta_2 != {}:
                for meta in meta_2:
                    print(meta['bibcode'])
                    try:
                        name = ARTICLES_DIR +  dir_name + '/' + meta['bibcode'] + '.pdf'
                        with open(name.replace('//', '/') , 'r') as f:
                            f.close()
                    except:
                        CatalogCollector().downloadPdfByBib(meta['bibcode'], ARTICLES_DIR +  dir_name, meta['bibcode'])



#https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/search/query
#https://github.com/adsabs/adsabs-dev-api/blob/master/API_documentation_Python/Search_API_Python.ipynb

#possible improvement
#https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp