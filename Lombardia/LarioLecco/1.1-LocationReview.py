import pandas as pd
locationList_ = pd.read_csv( 'Metadata/LocationList.csv' )
location= locationList_.groupby(['alias_city']).first()
locationList = location.copy().reset_index()
locationList['georeferencingString'] = locationList['alias_city']+", Lecco, Lombardia"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationListReviewed.csv',index=False)
