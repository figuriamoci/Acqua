import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/AceGasAmga')
print(os.getcwd())
gc.apply('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv')

#gc.retry('FriuliVeneziaGiulia/CAFC/Definitions/GeoReferencedLocationsList.csv')



