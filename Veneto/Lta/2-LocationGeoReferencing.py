import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Lta')
print(os.getcwd())
#gc.apply('Definitions/LocationList.csv','Definitions/GeoReferencedLocationsList.csv','')

gc.retry('Definitions/GeoReferencedLocationsList.csv')



