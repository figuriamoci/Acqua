import os
import acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/HydroGEA')
print(os.getcwd())
gc.apply('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv')

