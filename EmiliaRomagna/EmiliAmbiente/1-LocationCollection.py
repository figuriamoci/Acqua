import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "EmiliAmbiente"
aq.setEnv('EmiliaRomagna//'+gestore)
#url = 'https://www.emiliambiente.it/chi-siamo/qualita/la-qualita-dellacqua/'
urReport = 'https://www.emiliambiente.it/files/uploads/Tabelle-composizione-acqua-per-sito_II-semestre-2019.pdf'
locationList = pd.read_csv( 'Metadata/Alias_city.csv' )
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['georeferencingString']+", PR, Emilia Romagna"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
