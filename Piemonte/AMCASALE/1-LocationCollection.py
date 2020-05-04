import pandas as pd
import acqua.aqueduct as aq
gestore = "AMCASALE"
aq.setEnv('Piemonte//'+gestore)
alias_city = ['Balzola','Borgo San Martino','Bozzole','Caresana','Casale Monferrato(campo pozzi Terranova)','Casale Monferrato (campo pozzi Frassineto)','Costanzana','Frassineto Po','Giarole','Morano sul Po','Motta De Conti','Pertengo','Pezzana','Stroppiana','Ticineto','Valmacca','Villanova Monferrato']
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", AL, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)