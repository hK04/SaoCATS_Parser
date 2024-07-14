# SaoCATS_Parser
Project capable to automaticaly download and plot data from [SAO CATS Dataset](https://www.sao.ru/cats/) - Astrophysical CATalogs support System and find all data about original catalog (those catalogs data was copied into CATS) through [NASA ADS API](https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/search/query).

### Requirements 
```
astropy==5.2.1
matplotlib==3.5.2
numpy==4.1.5
selenium==1.21.5
pandas==1.4.2
```
### Architecture of project 

`main.py` - downloads all data (about ~6 thousand Radio Sources (AT20G publication) from CATS)

`parser.py` - selenium parser, could be used to download data from CATS independently of `main.py`

Input of `Searcher().search()` should consist of
`name`, `RAh`, `RAm`, `RAs`, `DE`, `DEd`, `DEm`, `DEs`, `Epoch` as it used in AT20G publication 
```
For example, input for:
J000012-853919	00.00.12.78-85.39.19.90

Should be looking like this:
(name='J000012-853919', RAh=0, RAm=0, RAs=12.78, DE='-', DEd=85, DEm=39, DEs=19.9, Epoch=2000)
```
