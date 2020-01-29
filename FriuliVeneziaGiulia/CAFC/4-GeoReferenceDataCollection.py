import os
import acqua.geoCode as gc
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
print(os.getcwd())
#c.apply('Definitions/ReviewedLocationList.csv','Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')

gc.retry('Definitions/GeoReferencedLocationsList.csv')


