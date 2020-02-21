import os,logging,pandas as pd,geojson
import acqua.geoCode as gc
os.chdir('/Users/andrea/PycharmProjects/Acqua/Lombardia/Milano')
logging.basicConfig(level=logging.INFO)

listaVieMM = pd.read_csv('Source/ds634_civici_coordinategeografiche_20200203.csv',delimiter=';')
campioneVieMM = listaVieMM.groupby('ID_NIL').last()

listAddress = campioneVieMM['TIPO'].str.lower()+' '+campioneVieMM['DESCRITTIVO'].str.lower()

locationList = pd.DataFrame({'alias_address':listAddress})
locationList['alias_city'] = 'Milano'
locationList['type'] = 'POINT'

locations = campioneVieMM['Location'].apply(lambda s: s.replace('(','').replace(')',''))
coordinates = locations.str.split(',')

#geoname = [gc.getGeoName(c) for c in list(coordinates)]
#locationList['georeferencingString'] = geoname

locationList['georeferencingString'] = '20100 MILANO, '+locationList['alias_address']
locationList.to_csv('Definitions/LocationList.csv',index=False)
