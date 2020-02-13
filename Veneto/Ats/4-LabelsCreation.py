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
##
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Ats')
logging.basicConfig(level=logging.DEBUG)
idGestore = 14211 #ALTO TREVIGIANO SERVIZI,
listParameters = parm.getListSynonyms('Definitions/SynParametri.csv')
parm.crea_dizionario('Definitions/SynParametri.csv')
##
import pickle
with open('Definitions/FoundReportList.pkl', 'rb') as f: foundReportList = pickle.load(f)

ll = []
#for report in foundReportList:
report = foundReportList[0]
rawData = report['parameters']

##
data = {'parameters':list(rawData[0].append(rawData[2])),'values':list(rawData[1].append(rawData[3]))}
labelData = pd.DataFrame(data)
labelData.set_index('parameters',inplace=True)
listParameters = ['PH','Durezza totale [°f]','Nitriti [mg/l]','Cloro residuo [mg/l]','Calcio [mg/l]','Cloruri [mg/l]','Solfato [mg/l]','Residuo fisso [mg/l]','Conducibilità [µS/cm]','Nitrati NO3 [mg/l]','Ammoniaca NH4 [mg/l]','Ferro [µg/l]','Magnesio [mg/l]','Floruri [mg/l]','Sodio [mg/l]',]
label = labelData.loc[listParameters]
data_report = 'oo'
lb = al.create_label( idGestore, data_report, label.to_dict() )

labelData


loc = (report['alias_city'],report['alias_address'])
glb = al.addGeocodeData( lb, loc, 'Definitions/GeoReferencedLocationsList.csv' )
logging.info( 'Georeferenced label for %s', idxRep )
for j in range( 0, len( glb ) ): ll.append( glb[j] )




##
reportFoundList = pd.read_csv('Definitions/FoundReportList.csv')
reportFoundList.set_index(['alias_city','alias_address','data_prelievo'],inplace=True)

xls = pd.read_csv( 'ReportAnalisiAltoAdige.csv' )

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





