import os,logging,acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/Poiana')
logging.basicConfig(level=logging.INFO)
gc.createGeoReferencedLocationsList('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv')
gc.findGeoName('Definitions/GeoReferencedLocationsList.csv')
gc.findGeometry('Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')

