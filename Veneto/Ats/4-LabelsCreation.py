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
listParameters = parm.getListSynonyms('Medadata/SynParametri.csv')
parm.crea_dizionario('Medadata/SynParametri.csv')
##
listParameters = ['PH','Durezza totale [°f]','Nitriti [mg/l]','Cloro residuo [mg/l]','Calcio [mg/l]','Cloruri [mg/l]','Solfato [mg/l]','Residuo fisso [mg/l]','Conducibilità [µS/cm]','Nitrati NO3 [mg/l]','Ammoniaca NH4 [mg/l]','Ferro [µg/l]','Magnesio [mg/l]','Floruri [mg/l]','Sodio [mg/l]',]
import pickle
with open('Definitions/FoundReportList.pkl', 'rb') as f: foundReportList = pickle.load(f)

ll = []
for report in foundReportList:
    #report = foundReportList[0]
    rawData = report['parameters']

    whereDataPrelievoIs = rawData.apply( lambda x: x.str.contains('Data Prelievo', na=False ) )
    alias_coordinates_ = np.where( whereDataPrelievoIs )
    alias_coordinates = (alias_coordinates_[0][0],alias_coordinates_[1][0])
    data_prelievo = rawData.iloc[alias_coordinates]

    data = {'parameters':list(rawData[0].append(rawData[2])),'values':list(rawData[1].append(rawData[3]))}
    labelData = pd.DataFrame(data)
    labelData.set_index('parameters',inplace=True)
    label = labelData.loc[listParameters].to_dict()['values']
    lb = al.create_label( idGestore, data_prelievo, label )

    loc = (report['alias_city'],report['alias_address'])
    glb = al.addGeocodeData( lb, loc, 'Medadata/GeoReferencedLocationsList.csv' )
    logging.info( 'Georeferenced label for %s', loc )
    for j in range( 0, len( glb ) ): ll.append( glb[j] )

##
#%%
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file(fc,'ATS.geojson')
coll.display(fc)
