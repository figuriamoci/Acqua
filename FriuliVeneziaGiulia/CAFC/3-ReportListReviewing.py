import os,logging
import pandas as pd
import numpy as np
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
foundReportList = pd.read_csv('Definitions/FoundReportList.csv')
foundReportList_ = foundReportList.copy()
foundReportList_['distincturl'] = foundReportList_['url']
reportStats = foundReportList_.groupby('alias_city').agg({'alias_address':'count','url':'count','distincturl':'nunique'})

citysReportUnico = reportStats[reportStats['distincturl']==1]
citysReportMultiplo = reportStats[reportStats['distincturl']>1]
citysReportAssente = reportStats[reportStats['distincturl']==0]

##
#Polygon
l = citysReportUnico.index.values
foundReportList_ = foundReportList.dropna()
dfPoligon_ = foundReportList_.loc[foundReportList_['alias_city'].isin(l)]
dfPoligon = dfPoligon_.groupby('alias_city').first()
dfPoligon.reset_index(inplace=True)
#Point
l = citysReportMultiplo.index.values
foundReportList_ = foundReportList.dropna()
dfPoint = foundReportList_.loc[foundReportList_['alias_city'].isin(l)]

dfFoundReportList = pd.concat([dfPoligon,dfPoint],sort=True)
dfFoundReportList.to_csv('Definitions/ReviewedReportList.csv',index=False)


listLocations = pd.read_csv('Definitions/LocationList.csv')
#####
#Quali solo i poligoni'
l = citysReportUnico.index.values
listLocations_ = listLocations.dropna()
dfPoligon_ = listLocations_.loc[listLocations_['alias_city'].isin(l)]
dfPoligon = dfPoligon_.groupby('alias_city').first()
dfPoligon.reset_index(inplace=True)
dfPoligon['type'] = 'POLYGON'
dfPoligon['georeferencingString'] = dfPoligon['alias_city']
#Quali solo i point?
l = citysReportMultiplo.index.values
dfPoint = listLocations.loc[listLocations['alias_city'].isin(l)]
dfPoint['type'] = 'POINT'
dfPoint.loc['georeferencingString'] = dfPoint['alias_city']+' '+dfPoint['alias_address']
#E gli atri?
l = citysReportAssente.index.values
listLocations_ = listLocations.dropna()
dfAltri_ = listLocations_.loc[listLocations_['alias_city'].isin(l)]
dfAltri = dfAltri_.groupby('alias_city').first()
dfAltri.reset_index(inplace=True)
dfAltri['type'] = 'POLYGON'
dfAltri['georeferencingString'] = dfPoligon['alias_city']
#Assembling
dfReviewedLocationList = pd.concat([dfPoligon,dfPoint,dfAltri],sort=True)
#Salva l'output
dfReviewedLocationList.to_csv('Definitions/ReviewedLocationList.csv',index=False)
logging.info('Safe %s geoquery location(s).',len(dfReviewedLocationList))

