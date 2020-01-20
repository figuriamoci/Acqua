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
import tabula,os,logging

logging.basicConfig(level=logging.DEBUG)
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/AceGasAmga')
idGestore = 926 ##AceGasAmga
data_report = 'Novembre 2019'
url = '2019_11_novembre_TS.1577977068.pdf'
listParameters = parm.getListSynonyms('Definitions/SynParametri.csv')
parm.crea_dizionario('Definitions/SynParametri.csv')
listLabels = {}
urlAndLocationList = {}
ll=[]
df = pd.read_csv('Definitions/FoundReportList.csv')
urlList = [url for url in df['url'].drop_duplicates()]
#Creazione del dizionario dei report e la lista di location associate.
for i,url in enumerate(urlList):
    locationList = df[df['url']==url].reindex(columns=['alias_city','alias_address'])
    locationListDict = locationList.to_dict(orient='records')
    urlAndLocationList[url]=locationListDict

##Conversione dei report in label
for url_report in urlList:

    #Reading table
    table_ = tabula.read_pdf( url_report, stream=True, pages="all" )
    table = table_.apply( lambda x: x.str.lower() )
    #Cleaning dataframe
    onlyTheseColumns = table[['parametro', 'valore']]
    cleaned_table = onlyTheseColumns.dropna( subset=['valore'] )
    onlyTheseParameters = cleaned_table.set_index( 'parametro' ).loc[listParameters].dropna()

    label = onlyTheseParameters['valore'].to_dict()

    lb = al.create_label( idGestore, data_report, label )
    locationList = urlAndLocationList[url_report]

    for location in locationList:
        x = location['alias_address']
        y = location['alias_city']
        location_ = (y, x)
        glb = al.addGeocodeData( lb, location_, 'Definitions/GeoReferencedLocationsList.csv' )
        ll.append( glb )

##
fc = coll.to_geojson(ll)
coll.to_file(fc,'AceGasAmga.geojson')
coll.display(fc)
