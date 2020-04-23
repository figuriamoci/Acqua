import pandas as pd,os
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC')
df_ = pd.read_csv('Definitions/GeoReferencedLocationsList.csv')
df = df_.copy()

a = df.loc[df['type']=='POLYGON']
df.loc[df['type']=='POLYGON',['geometry']]=''
b = df.loc[df['type']=='POLYGON']

df.to_csv('Medadata/GeoReferencedLocationsList.csv',index=False)