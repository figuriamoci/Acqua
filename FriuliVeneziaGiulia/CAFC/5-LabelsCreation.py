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
import tabula,os,logging,pickle

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
logging.basicConfig(level=logging.DEBUG)
idGestore = 12816
data_report = 'settembre 2919'
listParameters = parm.getListSynonyms('Definitions/SynParametri.csv')
parm.crea_dizionario('Definitions/SynParametri.csv')
listLabels = {}
ll=[]
urlAndLocationList = {}
df = pd.read_csv('Definitions/ReviewedReportList.csv')
####
urlList = [url for url in df['url'].drop_duplicates()]
##Creazione del dizionario dei report e la lista di location associate.
for i,url in enumerate(urlList):
    locationList = df[df['url']==url].reindex(columns=['alias_city','alias_address'])
    locationListDict = locationList.to_dict(orient='records')
    urlAndLocationList[url]=locationListDict

##Conversione dei report in label
for url_report in urlList:

    if url_report is np.nan:
        label = {}
        data_report = 'Parametri non disponinili'

    else:
        try:
            table_ = tabula.read_pdf(url_report, stream=True,pages="all")
            table = table_.apply(lambda x: x.str.lower())

            try:
                onlyTheseColumns = table[['Prova','Risultato']]
            except KeyError:
                onlyTheseColumns = table[['Prova U.M.', 'Risultato']]

            cleaned_table = onlyTheseColumns.dropna(subset=['Risultato'])

            try:
                onlyTheseParameters = cleaned_table.set_index('Prova').loc[listParameters].dropna()
            except KeyError:
                onlyTheseParameters = cleaned_table.set_index( 'Prova U.M.' ).loc[listParameters].dropna()

            label = onlyTheseParameters['Risultato'].to_dict()
            data_report = '09/12/2919'

            lb = al.create_label(idGestore,data_report,label)
            locationList = urlAndLocationList[url_report]

            for location in locationList:
                x = location['alias_address']
                y = location['alias_city']
                location_ = (y,x)
                glb = al.addGeocodeData(lb,location_,'Definitions/GeoReferencedLocationsList.csv')
                for i in range( 0, len( glb ) ): ll.append( glb[i] )
        except:
            logging.critical("The report '%s' was not readeble. Skipped!",url_report)

filename = 'ListLabels.pickle'
outfile = open(filename,'wb')
pickle.dump(ll,outfile)
outfile.close()
##
import pickle
filename = 'ListLabels.pickle'
infile = open(filename,'rb')
ll = pickle.load(infile)
infile.close()

a = ll[0]['geometry']


##
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file( fc, 'CAFC.geojson' )
coll.display(fc)

##

