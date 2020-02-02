import os
import acqua.geoCode as gc
import logging
logging.basicConfig(level=logging.INFO)

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Lta')
print(os.getcwd())
#gc.apply('Definitions/GeoReferencingLocationList.csv','Definitions/GeoReferencedLocationsList.csv','none')

gc.retry('Definitions/GeoReferencedLocationsList.csv')



