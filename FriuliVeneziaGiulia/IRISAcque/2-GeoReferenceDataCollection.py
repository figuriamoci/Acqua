import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque')
logging.info(os.getcwd())

gc.createGeoReferencedLocationsList('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv')
gc.findGeoName('Definitions/GeoReferencedLocationsList.csv')
gc.findGeometry('Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')


