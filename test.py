import pandas as pd
datiGeo = pd.read_csv('Definitions/GeoReferencedLocationsList.csv')
datiGeo = datiGeo.set_index('name')
datiGeo = datiGeo.to_dict(orient='index')
#Recupera dati geo di tipo Point
label,name

geocode = datiGeo['alias']['geocode']
latitude = datiGeo[label.getAlias()]['latitude']
longitude = datiGeo[label.getAlias()]['longitude']