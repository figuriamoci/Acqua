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
import tabula
import os
import logging
#os.chdir('D:/Python/Acqua/')
os.chdir('/Users/andrea/PycharmProjects/Acqua')
idGestore = 13146
parm.crea_dizionario('FriuliVeneziaGiulia/HydroGEA/Definitions/SynParametri.csv')
data_report = '30-02-1900'
##
def get_rawTable(url_report):
    import tabula
    row_table = tabula.read_pdf(url_report, stream=True,pages="all")
    row_table2 = row_table.T.reset_index().T
    return row_table2

def estractLabelFromRawTable(address,rawTable):
    parms = ['ph', 'Residuo fisso a 180°', 'Resid. fisso 180°', 'Durezza', 'Conducibilità', 'Calcio', 'Magnesio',
             'Ammonio', 'Cloruri',
             'Solfati', 'Potassio', 'Sodio', 'Arsenico', 'Bicarbonato', 'Cloro residuo', 'Fluoruri', 'Nitrati',
             'Nitriti',
             'Manganese']
    import numpy as np
    table_ = rawTable.reset_index()
    #table_.to_csv('table_.csv')
    logging.info('Searcing for address... %s.', address)
    boolMatrix = table_.apply(lambda x: x.str.contains(address, na=False))
    alias_coordinates_ = np.where(boolMatrix)
    if len(alias_coordinates_[0])==0 or len(alias_coordinates_[1])==0: raise AddressNotFound("%s not found.",address)
    alias_coordinates = [x[0] for x in alias_coordinates_]
    alias_address = table_.iloc[alias_coordinates]
    rowFound = alias_coordinates[0]
    columnFound = alias_coordinates[1]
    logging.info('Found address %s. at [%s,%s].', address,rowFound,columnFound)
    table_.set_index(0,inplace=True)
    label = table_.reindex(index=parms,columns=[columnFound-1])
    label_cleaned = label.dropna()
    label_cleaned.columns = ['label']
    lbdict = label_cleaned['label'].to_dict()
    ll = {}
    ll['alias_address'] = address
    ll['label'] = lbdict
    logging.info('Creating label %s.', ll)
    return ll
##
#data_report = 'settembre 2919'
#listParameters = ['Concentrazione di ioni idrogeno','Conduttività a 20° C','* Calcio (Ca)','* Magnesio (Mg)','Durezza (da calcolo)','Fluoruro','Nitrato','Cloruro','Solfati','*  Sodio (Na)','*  Potassio (K)','Manganese (Mn)','Nitrito','Ammonio','Arsenico (As)','* Residuo fisso a 180 °C']
#listLabels = {}
##
#print(os.path.abspath('FriuliVeneziaGiulia/HydroGEA/Definitions/FoundReportList.csv'))
logging.basicConfig(level=logging.DEBUG)
df = pd.read_csv('FriuliVeneziaGiulia/HydroGEA/Definitions/FoundReportList.csv')
df = df.set_index(['alias_city','alias_address'])
locationList = df.index
logging.info('Caricato la FoundReportList.csv con %s elementi.',len(df))
##
#logging.basicConfig(level=logging.DEBUG)
ll = []
i=0
for location in locationList:
    i=i+1
    logging.info('Ricerca etichetta per %s. (Progress %s/%s)', location,i,len(locationList))
    address = location[1]
    city = location[0]
    urlReport_ = df.loc[location,'urlReport']
    urlReport = urlReport_.replace('%20',' ')
    rawTable = get_rawTable(urlReport)
    try:
        rawLabel = estractLabelFromRawTable(address,rawTable)
        label = rawLabel['label']
        lb = al.create_label(idGestore,data_report,label)
        glb = al.addGeocodeData(lb,location,'FriuliVeneziaGiulia/HydroGEA/Definitions/GeoReferencedLocationsList.csv')
        ll.append(glb)
    except:
        logging.critical('Skip label for %s',location)

##
fc = coll.to_geojson(ll)
coll.to_file(fc,'FriuliVeneziaGiulia/HydroGEA/HydroGEA.geojson')
coll.display(fc)

logging.info('Created %s label(s) of %s.',len(ll),len(locationList))
logging.info('End process.')
