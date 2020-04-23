import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque')
logging.info(os.getcwd())

gc.createGeoReferencedLocationsList('Medadata/LocationList.csv','Medadata/GeoReferencedLocationsList.csv')
gc.findGeoName('Medadata/GeoReferencedLocationsList.csv')
gc.findGeometry('Medadata/GeoReferencedLocationsList.csv','Medadata/ConfiniComuniFVG.geojson')


