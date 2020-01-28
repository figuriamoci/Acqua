import os
import acqua.geoCode as gc
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
print(os.getcwd())
gc.apply('Definitions/GeoReferencingLocationList.csv','Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')

#gc.retry('FriuliVeneziaGiulia/CAFC/Definitions/GeoReferencedLocationsList.csv')


