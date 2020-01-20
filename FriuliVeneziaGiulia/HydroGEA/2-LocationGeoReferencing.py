import os
import acqua.geoCode as gc

os.chdir('/Users/andrea/PycharmProjects/Acqua/')
print(os.getcwd())
gc.apply('FriuliVeneziaGiulia/HydroGEA/Definitions/LocationList.csv','FriuliVeneziaGiulia/HydroGEA/Definitions/GeoReferencedLocationsList.csv')

