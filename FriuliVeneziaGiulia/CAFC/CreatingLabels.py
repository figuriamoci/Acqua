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


idGestore = 12816
gestoreAcqua = 'CAFC S.P.A.'
sito_internet = 'https://www.cafcspa.com'
data_report = 'settembre 2919'
listParameters = ['Concentrazione di ioni idrogeno','Conduttività a 20° C','* Calcio (Ca)','* Magnesio (Mg)','Durezza (da calcolo)','Fluoruro','Nitrato','Cloruro','Solfati','*  Sodio (Na)','*  Potassio (K)','Manganese (Mn)','Nitrito','Ammonio','Arsenico (As)','* Residuo fisso a 180 °C']
listLabels = {}

df = pd.read_csv('Definitions/LocationList.csv')
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
print(fc)
coll.display(fc)
