import os,logging,acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Ats')
logging.basicConfig(level=logging.INFO)
#gc.createGeoReferencedLocationsList('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv')
#gc.findGeoName('Definitions/GeoReferencedLocationsList.csv')
gc.findCoordinates('Definitions/GeoReferencedLocationsList.csv')
