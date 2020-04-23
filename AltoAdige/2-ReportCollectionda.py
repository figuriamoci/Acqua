import os,logging,pandas as pd
os.chdir('/Users/andrea/PycharmProjects/Acqua/AltoAdige' )
logging.basicConfig(level=logging.INFO)

xls = pd.read_csv( 'ReportAnalisiAltoAdige.csv' )

alias_city = xls['Comune / Gemeinde']
alias_address = xls['Punto di prelievo / Entnahmepunkt']
data_prelievo = pd.to_datetime(xls['Data prelievo / Entnahme Datum ']).dt.strftime('%d/%m/%Y')

data = {'alias_city':alias_city, 'alias_address':alias_address,'data_prelievo':data_prelievo}
df_ = pd.DataFrame(data)

df = df_.groupby(['alias_city','alias_address'])['data_prelievo'].max()
fl = df.reset_index()
fl.to_csv('Medadata/DataReportCollection.csv',index=False)