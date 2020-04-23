import logging,pandas as pd
import acqua.aqueduct as aq
aq.setEnv('Lombardia//MM')

listaVieMM = pd.read_csv('Source/ds634_civici_coordinategeografiche_20200203.csv',delimiter=';')
campioneVieMM = listaVieMM.groupby('ID_NIL').last()

listAddress = campioneVieMM['TIPO'].str.lower()+' '+campioneVieMM['DESCRITTIVO'].str.lower()

locationList = pd.DataFrame({'alias_address':listAddress})
locationList['alias_city'] = 'MM'
locationList['type'] = 'POINT'

locations = campioneVieMM['Location'].apply(lambda s: s.replace('(','').replace(')',''))
coordinates = locations.str.split(',')

locationList['georeferencingString'] = '20100 MILANO, '+locationList['alias_address']
locationList.to_csv('Medadata/LocationList.csv',index=False)
