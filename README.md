# SaoCATS_Parser
Selenium application to automaticaly download and plot data from [SAO CATS Dataset](https://www.sao.ru/cats/) - Astrophysical CATalogs support System

### Requirements 
```
astropy==5.2.1
matplotlib==3.5.2
numpy==4.1.5
selenium==1.21.5
pandas==1.4.2
```
### Usage 
Currently `parser.py` nicely usable only for Radio sources.

#### Input should consist of
`name`, `RAh`, `RAm`, `RAs`, `DE`, `DEd`, `DEm`, `DEs`, `Epoch` as it used in AT20G catalog 

```
For example, input for:
J000012-853919	00.00.12.78-85.39.19.90

Should be looking like this:
(name='J000012-853919', RAh=0, RAm=0, RAs=12.78, DE='-', DEd=85, DEm=39, DEs=19.9, Epoch=2000)
```
