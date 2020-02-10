#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:52:40 2020

@author: andrea
"""
##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import pandas as pd
import numpy as np
import os,logging,datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium import webdriver
##
os.chdir('/Users/andrea/PycharmProjects/Acqua/AltoAdige')
logging.basicConfig(level=logging.DEBUG)
idGestore = 993 #Provincia Autonoma Alto Adige
listParameters = parm.getListSynonyms('Definitions/SynParametri.csv')
parm.crea_dizionario('Definitions/SynParametri.csv')
##
reportFoundList = pd.read_csv('Definitions/FoundReportList.csv')
reportFoundList.set_index(['alias_city','alias_address','data_prelievo'],inplace=True)

xls = pd.read_csv('Definitions/ReportAnalisiAltoAdige.csv')

df = xls.rename(columns={'Comune / Gemeinde':'alias_city','Punto di prelievo / Entnahmepunkt':'alias_address'})
df['data_prelievo'] = pd.to_datetime(xls['Data prelievo / Entnahme Datum ']).dt.strftime('%d/%m/%Y')
df.set_index(['alias_city','alias_address','data_prelievo'],inplace=True)
##
listParameters = ['Durezza totale F°','pH','Sodiomg/L','Solfati mg/L','Nitrati NO3 mg/L','Nitriti NO2 mg/L','Cloruri mg/L','Conduc. Elettr. Spec.µS/cm','Fluoruri mg/L','Ammonio NH4 mg/L','Manganese µg/L','Arsenico µg/L','Ferro µg/L']
rawTable = df[listParameters]
ll = []
for idxRep in reportFoundList.index:
    logging.info('Extracting label for %s',idxRep)
    rawLabel_ = rawTable.loc[idxRep]
    for idxRep, rawLabel in rawLabel_.iterrows():
        label = rawLabel.to_dict()
        data_report = idxRep[2]
        lb = al.create_label( idGestore, data_report, label )
        logging.info( 'Created label for %s',idxRep)
        loc = (idxRep[0],idxRep[1])
        glb = al.addGeocodeData( lb, loc, 'Definitions/GeoReferencedLocationsList.csv' )
        logging.info( 'Georeferenced label for %s', idxRep )
        for j in range( 0, len( glb ) ): ll.append( glb[j] )
##
logging.info('End.')
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file(fc,'AltoAdige.geojson')
coll.display(fc)





