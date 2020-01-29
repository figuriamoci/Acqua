import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque')
logging.info(os.getcwd())

gc.apply('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv','Definitions/ConfiniComuniFVG.geojson')

#gc.retry('FriuliVeneziaGiulia/CAFC/Definitions/GeoReferencedLocationsList.csv')
