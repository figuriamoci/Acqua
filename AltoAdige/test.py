import os,logging,pandas as pd
os.chdir('/Users/andrea/PycharmProjects/Acqua/AltoAdige' )
logging.basicConfig(level=logging.INFO)

xls_file = 'Definitions/03__Internet-tabella_2018-2017-2016-.xlsx'
xl = pd.read_excel(xls_file, index_col=0)
xl.reset_index(inplace=True)
xl.dropna(axis=0,subset=['Comune / Gemeinde'],inplace=True)

alias_city = xl['Comune / Gemeinde']
alias_address = xl['Punto di prelievo / Entnahmepunkt']
data_prelievo = pd.to_datetime(xl['Data prelievo / Entnahme Datum ']).dt.strftime('%d/%m/%Y')
data = {'alias_city':alias_city, 'alias_address':alias_address,'data_prelievo':data_prelievo}
df_ = pd.DataFrame(data)

df = df_.groupby(['alias_city','alias_address']).min()
df.reset_index(inplace=True)
df['georeferencingString'] = df['alias_city'].apply(lambda s: s.split('/')[0])+' '+df['alias_address'].apply(lambda s: s.split('/')[0])
df['type']='POINT'
df.to_csv('a.csv',index=False)



    .max()
a.set_index(['Comune / Gemeinde','Punto di prelievo / Entnahmepunkt','Data prelievo'],inplace=True)
b = a[['Comune / Gemeinde','Punto di prelievo / Entnahmepunkt','Data prelievo']]
b.to_csv('a.csv',index=False)

#a = xl.loc[xl.groupby(['Comune / Gemeinde','Punto di prelievo / Entnahmepunkt'])['Data prelievo'].idmax()]


a['Data prelievo'].max(axis=0, skipna=True)


b = a['Data prelievo / Entnahme Datum'].idmax()






alias_city_ = xl['Comune / Gemeinde']
alias_address_ = xl['Punto di prelievo / Entnahmepunkt']

##
data = {'alias_city':alias_city_,'alias_address':alias_address_}
df = DataFrame = pd.DataFrame(data)
df['georeferencingString'] = df['alias_city'].apply(lambda s: s.split('/')[0])+' '+df['alias_address'].apply(lambda s: s.split('/')[0])
df['type']='POINT'
#DataCleaning on georeferencingString...
listRemoveString = ['rubinetto cucina','Fontana pubblica','Fontana Pubblica','Oberradein','Kirchplatz','piazza paese','centro paese','vicino chiesa','vicino','davanti','Brennerhof','Gasthof','Oberradein',
                    'di lingua italiana','Unterhausenhof','neben FF Montiggl','Öffentl.','Comune','incrocio','Privato']

for rs in listRemoveString:
    df['georeferencingString'] = df['georeferencingString'].apply(lambda s: s.replace( rs, '' ).strip() )

df.to_csv('Definitions/LocationList.csv',index=False)