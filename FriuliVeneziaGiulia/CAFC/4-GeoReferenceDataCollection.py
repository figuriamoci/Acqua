import os
import acqua.geoCode as gc
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
print(os.getcwd())
#gc.apply('Medadata/ReviewedLocationList.csv','Medadata/GeoReferencedLocationsList.csv','Medadata/ConfiniComuniFVG.geojson')

#gc.findGeoName('Medadata/GeoReferencedLocationsList.csv')
gc.findGeometry('Medadata/GeoReferencedLocationsList.csv','Medadata/ConfiniComuniFVG.geojson')



