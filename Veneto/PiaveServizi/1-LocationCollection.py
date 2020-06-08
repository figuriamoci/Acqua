##
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "PiaveServizi"
aq.setEnv('Veneto//'+gestore)
locationList = pd.read_csv('Metadata/AqueductList.csv')
locationList['georeferencingString'] = locationList['alias_address'].replace('Comune','')+", "+locationList['alias_city']+", TV, Veneto"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)

