import pandas as pd
import acqua.aqueduct as aq
gestore = "ASVTValtrompia"
aq.setEnv('Lombardia//'+gestore)
LocationList = pd.read_csv("Metadata/LocationList.csv")
df_ = LocationList.groupby(['alias_city','alias_address']).count()['georeferencingString']
locationListReviewed = df_.reset_index()[['alias_city','alias_address']]
locationListReviewed['georeferencingString'] = locationListReviewed['alias_address']+", "+locationListReviewed['alias_city']+", BS, Lombardia"
locationListReviewed['type'] = 'POINT'
locationListReviewed.to_csv('Metadata/ReviewedLocationList.csv',index=False)