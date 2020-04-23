import os,logging,acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/Poiana')
logging.basicConfig(level=logging.INFO)
gc.createGeoReferencedLocationsList('Medadata/LocationList.csv','Medadata/GeoReferencedLocationsList.csv')
gc.findGeoName('Medadata/GeoReferencedLocationsList.csv')
gc.findGeometry('Medadata/GeoReferencedLocationsList.csv','Medadata/ConfiniComuniFVG.geojson')

