import os,logging,acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/AltoAdige')
logging.basicConfig(level=logging.INFO)
#gc.createGeoReferencedLocationsList('Medadata/LocationList.csv','Medadata/GeoReferencedLocationsList.csv')
#gc.findGeoName('Medadata/GeoReferencedLocationsList.csv')
gc.findGeometry('Medadata/GeoReferencedLocationsList.csv','')


import pandas as pd
geoRLL = pd.read_csv('Definitions/GeoReferencedLocationsList.csv')
howManyGeoCode = geoRLL.groupby('alias_city').count()['geocode']
howManyGeoCode = howManyGeoCode.to_frame()
howNull = howManyGeoCode[howManyGeoCode['geocode']==0]
print(howNull)