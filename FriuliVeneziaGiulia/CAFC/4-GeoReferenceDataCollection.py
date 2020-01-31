import os
import acqua.geoCode as gc
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
print(os.getcwd())
#gc.apply('Definitions/ReviewedLocationList.csv','Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')

#gc.findGeoName('Definitions/GeoReferencedLocationsList.csv')
gc.findGeometry('Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')



