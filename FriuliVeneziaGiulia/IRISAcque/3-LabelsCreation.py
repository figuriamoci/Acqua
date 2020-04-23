#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:52:40 2020

@author: andrea
"""
##
import camelot,os,logging
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import pandas as pd
import numpy as np
#Inizializazione ambiemte
logging.basicConfig(level=logging.DEBUG)
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque')
#Algoritmo
idGestore = 7396 ##IRISAcque
dataReport='ANNO 2019 I SEMESTRE'

#Inizializzazone robot
listParameters = parm.getListSynonyms('Medadata/SynParametri.csv')
parm.crea_dizionario('Medadata/SynParametri.csv')
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
    tables = camelot.read_pdf( url_report )
    logging.info(tables[0].parsing_report)
    table_ = tables[0].df

    #tables.export( 'foo.csv', f='csv', compress=False )  # json, excel, html

    table = table_.apply( lambda x: x.str.lower() )
    table = table.apply( lambda x: x.replace('\n','') )

    locationAlias = table.iloc[0, 3:]
    locationAlias = locationAlias.apply( lambda x: x.replace( '\n', '' ) )
    cleaned_table = table.drop( [0, 1], axis=0 )  # Rimosse due righe
    cleaned_table = cleaned_table.drop( [1, 2], axis=1 )  # Rimosse 1 riga
    cleaned_table = cleaned_table.set_index( 0 )
    cleaned_table.columns = locationAlias  # colonne impostate con i parametri

    #lb = al.create_label( idGestore, data_report, label )
    locationList = urlAndLocationList[url_report]

    for location in locationList:
        x = location['alias_address']
        y = location['alias_city']
        location_ = (y, x)
        label = cleaned_table[y.lower()].to_dict()
        lb = al.create_label( idGestore, dataReport, label )
        glb = al.addGeocodeData( lb, location_, 'Medadata/GeoReferencedLocationsList.csv' )
        for i in range( 0, len( glb ) ): ll.append( glb[i] )

fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file(fc,'IRISAcque.geojson')
coll.display(fc)


