#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:52:40 2020

@author: andrea
"""
import acqua.label as al
import acqua.labelCollection as coll
import pandas as pd
import tabula
import os


idGestore = 12816
gestoreAcqua = 'CAFC S.P.A.'
sito_internet = 'https://www.cafcspa.com'
data_report = 'settembre 2919'
listParameters = ['Concentrazione di ioni idrogeno','Conduttività a 20° C','* Calcio (Ca)','* Magnesio (Mg)','Durezza (da calcolo)','Fluoruro','Nitrato','Cloruro','Solfati','*  Sodio (Na)','*  Potassio (K)','Manganese (Mn)','Nitrito','Ammonio','Arsenico (As)','* Residuo fisso a 180 °C']
listLabels = {}

print(os.path.abspath("Definitions/FoundReportList.csv"))
df = pd.read_csv('Definitions/FoundReportList.csv')
ll=[]

dx = df.pivot(index='url', columns='location')
listReports = dx.index
url_report = listReports[0]
#report = 'https://www.cafcspa.com/solud/analisi/D702.pdf'
    
table = tabula.read_pdf(url_report, stream=True,pages="all")
onlyTheseColumns = table[['Prova','Risultato']]
cleaned_table = onlyTheseColumns.dropna(subset=['Risultato'])
onlyTheseParameters = cleaned_table.set_index('Prova').loc[listParameters]
label = onlyTheseParameters['Risultato'].to_dict()
  
lb = al.create_label(gestoreAcqua,data_report,label)
    
for location in df['location']:
    glb = al.addGeocodeData(lb,location)
    ll.append(glb)
    print(location)
    
fc = coll.to_geojson(ll)
mdb = coll.to_MDBCollection(ll)


#file = open('forMongDB.json', 'w')
#file.write(glb)
#file.close()
print(glb)

#import pymongo as py
#conn = py.MongoClient("mongodb+srv://Acqua:nato1968@principal-4g7w8.mongodb.net/test?retryWrites=true&w=majority")
#db = conn.Acqua
#collection = db.etichette
#collection.insert_many(ll)


print(fc)
coll.display(fc)
