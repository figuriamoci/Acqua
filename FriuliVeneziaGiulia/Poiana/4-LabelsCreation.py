# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:24:21 2020

@author: 912522
"""
import tabula,os
import acqua.label as al
import acqua.parametri as parm
import acqua.labelCollection as coll
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/Poiana')
url = 'Definitions/Acque Potabili - Analisi Chimico fisiche 2018_2019.pdf'
GeoReferencedLocationsList = 'Definitions/GeoReferencedLocationsList.csv'

idGestore = 15123 ##Poiana
#listParameters = parm.getListSynonyms('Definitions/SynParametri.csv')
parm.crea_dizionario('Definitions/SynParametri.csv')
tables = tabula.read_pdf(url,multiple_tables=True,pages='all',encoding='utf-8')
#%%
listRawtables = []
for table in tables:
    sx = table.iloc[:,0:2]
    listRawtables.append(sx)
    dx = table.iloc[:,2:4]
    listRawtables.append(dx)    
#%%
ll = []
for rt in listRawtables:
    if rt.shape == (19, 2):
        #rt = listRawtables[0]
        alias_city = rt.iloc[2,0]
        alias_address = rt.iloc[1,0]
        data_report = rt.iloc[1,1]
        #Estrazione parametri
        parametri = rt.iloc[4:,0].to_list()
        valori_ = rt.iloc[4:,1].to_list()
        valori = [v.split(' ')[0] for v in valori_]
        label = {p:valori[i] for i,p in enumerate(parametri)}
        #Creazione etichetta
        lb = al.create_label(idGestore, data_report, label )
        #Georeferenzazione
        location = (alias_city, alias_address)
        glb = al.addGeocodeData( lb, location, GeoReferencedLocationsList )
        for i in range( 0, len( glb ) ): ll.append( glb[i] )
    
#%%
fc = coll.to_geojson(ll,rgb=coll.getRGB())
coll.to_file(fc,'Poiana.geojson')
coll.display(fc)
