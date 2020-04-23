import os,logging,pandas as pd
os.chdir('/Users/andrea/PycharmProjects/Acqua/Lombardia/GruppoCAP')
logging.basicConfig(level=logging.INFO)

df = pd.read_csv('Source/Medie ponderate comuni 2018.csv',sep=';',keep_default_na=False,thousands='.',decimal=',')
reportFound = df[1:]

loctionList = pd.DataFrame()
loctionList['alias_city'] = reportFound['Comune']
loctionList['alias_address'] = 'Territorio comunale'
loctionList['georeferencingString'] = reportFound['Comune']+' MI'
loctionList['tyoe'] = 'POINT'

loctionList.to_csv('Medadata/LocationList.csv',index=False)



