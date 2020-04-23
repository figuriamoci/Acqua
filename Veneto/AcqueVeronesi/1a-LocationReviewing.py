import pandas as pd
import acqua.aqueduct as aq
aq.setEnv('Veneto//AcqueVeronesi')

df = pd.read_csv('Definitions/LocationList.csv')
dfRevied_ = df.groupby(['alias_city']).first()
dfRevied = dfRevied_.copy()
dfRevied.reset_index(inplace=True)

dfRevied.to_csv('Medadata/ReviewedLocationList.csv',index=False)