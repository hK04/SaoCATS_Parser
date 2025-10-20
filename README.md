# SaoCATS_Parser
Project to help you to automaticaly download and plot astrophyiscal data from [SAO CATS Dataset](https://www.sao.ru/cats/) - Astrophysical CATalogs support System and also, to find all data about original catalogs (of these catalogs which was copied into CATS) through [NASA ADS API](https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/search/query).

### 1. Requirements 
```
astropy==5.2.1
matplotlib==3.5.2
numpy==4.1.5
selenium==1.21.5
pandas==1.4.2
```
### 2. Architecture of project: 

```
parser.py - selenium parser's backbone 
main.py - downloads all data (about ~6 thousand Radio Sources from AT20G publication with CATS database)
```

### 3. Usage:



>Input of `Searcher().search()` should consist of
>`name`, `RAh`, `RAm`, `RAs`, `DE`, `DEd`, `DEm`, `DEs`, `Epoch` as it used in AT20G publication 

For example, input for:
`J000012-853919 00.00.12.78-85.39.19.90`

Should be looking like this:

```python
(name='J000012-853919',
  RAh=0, 
  RAm=0, 
  RAs=12.78,
  DE='-', 
  DEd=85, 
  DEm=39, 
  DEs=19.9, 
  Epoch=2000
)
```
