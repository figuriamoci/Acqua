import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia')
print(os.getcwd())


gc.apply('IRISAcque/Definitions/LocationList.csv','IRISAcque/Definitions/GeoReferencedLocationsList.csv')

#gc.retry('FriuliVeneziaGiulia/CAFC/Definitions/GeoReferencedLocationsList.csv')
