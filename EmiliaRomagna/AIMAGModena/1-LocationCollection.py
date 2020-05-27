import pandas as pd
import acqua.aqueduct as aq
url = 'https://www.aimag.it/cosa-facciamo/ciclo-idrico-integrato/controlli-acqua/'
gestore = "AIMAGModena"
aq.setEnv('EmiliaRomagna//'+gestore)
#
city = pd.read_csv('Metadata/Alias_city.csv')
alias_city = city['alias_city']
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", Emilia Romagna"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
