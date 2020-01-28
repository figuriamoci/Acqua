import os
import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
foundReportList = pd.read_csv('Definitions/FoundReportList.csv')
foundReportList_ = foundReportList.copy()
foundReportList_['distincturl'] = foundReportList_['url']
reportStats = foundReportList_.groupby('alias_city').agg({'alias_address':'count','url':'count','distincturl':'nunique'})

citysReportUnico = reportStats[reportStats['distincturl']==1]
citysReportMultiplo = reportStats[reportStats['distincturl']>1]
citysReportAssente = reportStats[reportStats['distincturl']==0]

listLocations = pd.read_csv('Definitions/LocationList.csv')
listLocations['type']=np.nan
#Quali solo i poligoni'
l = citysReportUnico.index.values
listLocations.loc[listLocations['alias_city'].isin(l),'type'] = 'POLYGON'
#Quali solo i point?
l = citysReportMultiplo.index.values
listLocations.loc[listLocations['alias_city'].isin(l),'type'] = 'POINT'
#E gli atri?
l = citysReportAssente.index.values
listLocations.loc[listLocations['alias_city'].isin(l),'type'] = 'POLYGON'
#Cleaning
listLocations.dropna(inplace=True)
#listLocations
#listLocations.drop('georeferencingString',axis=1,inplace=True)
listLocations['georeferencingString'] = np.where(listLocations['type']=='POLYGON', listLocations['alias_city'] , listLocations['alias_city']+' '+listLocations['alias_address'])
#Salva l'output
listLocations.to_csv('Definitions/GeoReferencingLocationList.csv',index=False)
logging.info('Safe %s geoquery location(s).',len(listLocations))

