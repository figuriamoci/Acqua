import os,logging,acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/AltoAdige')
logging.basicConfig(level=logging.INFO)
#gc.createGeoReferencedLocationsList('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv')
#gc.findGeoName('Definitions/GeoReferencedLocationsList.csv')
gc.findGeometry('Definitions/GeoReferencedLocationsList.csv','')


import pandas as pd
geoRLL = pd.read_csv('Definitions/GeoReferencedLocationsList.csv')
howManyGeoCode = geoRLL.groupby('alias_city').count()['geocode']
howManyGeoCode = howManyGeoCode.to_frame()
howNull = howManyGeoCode[howManyGeoCode['geocode']==0]
print(howNull)