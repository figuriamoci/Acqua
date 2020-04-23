import os
import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Lta')
#
locationList = pd.read_csv('Definitions/LocationList.csv')
locationList['type']='POINT'
locationList['georeferencingString']=locationList['alias_address'].apply(lambda x: x.replace('-',''))
locationList['georeferencingString']=locationList['georeferencingString'].apply(lambda x: x.replace('mini acquedotto',''))
locationList['georeferencingString']=locationList['georeferencingString'].apply(lambda x: x.replace('loc.',''))
#Salva l'output
locationList.to_csv('Medadata/GeoReferencingLocationList.csv',index=False)
logging.info('Safe %s geoquery location(s).',len(locationList))

