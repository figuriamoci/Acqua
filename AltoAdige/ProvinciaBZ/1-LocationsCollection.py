import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "ProvinciaBZ"
aq.setEnv('AltoAdige//'+gestore)
logging.basicConfig(level=logging.INFO)

xls_file = 'DataSource/03__Internet-tabella_2018-2017-2016-.xlsx'
xls = pd.read_excel(xls_file, index_col=0)
xls.reset_index(inplace=True)
xls.dropna(axis=0,subset=['Comune / Gemeinde'],inplace=True)
xls.columns = xls.columns.str.replace('\n','')
xls.sort_values(by=['Comune / Gemeinde','Punto di prelievo / Entnahmepunkt','Data prelievo / Entnahme Datum '], inplace=True)
xls.to_csv('Metadata/ReportAnalisiAltoAdige.csv',index=False)
#
alias_city = xls['Comune / Gemeinde']
alias_address = xls['Punto di prelievo / Entnahmepunkt']
data_prelievo = pd.to_datetime(xls['Data prelievo / Entnahme Datum ']).dt.strftime('%d/%m/%Y')
#
data = {'alias_city':alias_city, 'alias_address':alias_address,'data_report':data_prelievo}
df_ = pd.DataFrame(data)
df = df_.groupby(['alias_city','alias_address']).min()
df.reset_index(inplace=True)
df['georeferencingString'] = df['alias_city'].apply(lambda s: s.split('/')[0])+' '+df['alias_address'].apply(lambda s: s.split('/')[0])
df['type']='POINT'
#DataCleaning on georeferencingString...
listRemoveString = ['rubinetto cucina','Fontana pubblica','Fontana Pubblica','Oberradein','Kirchplatz','piazza paese','centro paese','vicino chiesa','vicino','davanti','Brennerhof','Gasthof','Oberradein','di lingua italiana','Unterhausenhof','neben FF Montiggl','Öffentl.','Comune','incrocio','Privato']
for rs in listRemoveString: df['georeferencingString'] = df['georeferencingString'].apply(lambda s: s.replace( rs, '' ).strip() )
df.to_csv('Metadata/LocationList.csv',index=False)