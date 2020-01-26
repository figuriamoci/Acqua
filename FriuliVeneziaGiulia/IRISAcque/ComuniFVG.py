# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:01:36 2020

@author: 912522
"""
import os
import geojson as json
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque')

listComuni = ["CAPRIVA DEL FRIULI","CORMONS","DOBERDO' DEL LAGO","DOLEGNA DEL COLLIO","FARRA D'ISONZO","FOGLIANO REDIPUGLIA","GORIZIA","GRADISCA D'ISONZO","GRADO","MARIANO DEL FRIULI","MEDEA","MONFALCONE","MORARO","MOSSA","ROMANS D'ISONZO","RONCHI DEI LEGIONARI","SAGRADO","SAN CANZIAN D'ISONZO","SAN FLORIANO DEL COLLIO","SAN LORENZO ISONTINO","SAN PIER D'ISONZO","SAVOGNA D'ISONZO","STARANZANO","TURRIACO","VILLESSE"]

with open('Definitions/ConfiniComuniFVG.geojson') as data_file: data = json.load(data_file)
feature_collection = json.FeatureCollection(data)
ListFeatures = feature_collection['features']
comune = 'AIELLO DEL FRIULI'

c = {}
for comune in listComuni:
    matches = [x for i,x in enumerate(ListFeatures) if a[i]['properties']['name']==comune]
    c[comune] = matches

print(c['CORMONS'])

x = c['CORMONS'][0]['geometry']['coordinates']
y = c['MEDEA'][0]['geometry']['coordinates']

Acquedottistico3 = sorted(list(set(x)) + list(set(y)))


import pandas as pd
data = [['tom', 10, ['andrea','fantini']], ['nick', 15, ['andrea','fantini']], ['juli', 14,['Fiorella','marchiori','marco']]] 
df = pd.DataFrame(data, columns = ['Name', 'Age','set'])
df.to_csv('df_exaple.csv')
fd = pd.read_csv('df_exaple.csv')

q = fd['set']
print(q.loc[0])
ii = q.loc[0]
for i in ii: print(i)

