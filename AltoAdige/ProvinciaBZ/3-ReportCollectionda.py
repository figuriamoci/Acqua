import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "ProvinciaBZ"
aq.setEnv('AltoAdige//'+gestore)
logging.basicConfig(level=logging.INFO)
#
xls = pd.read_csv( 'ReportAnalisiAltoAdige.csv' )
#
alias_city = xls['Comune / Gemeinde']
alias_address = xls['Punto di prelievo / Entnahmepunkt']
data_report = pd.to_datetime(xls['Data prelievo / Entnahme Datum ']).dt.strftime('%d/%m/%Y')
#
data = {'alias_city':alias_city, 'alias_address':alias_address,'data_report':data_report}
df_ = pd.DataFrame(data)
df = df_.groupby(['alias_city','alias_address'])['data_report'].max()
fl = df.reset_index()
fl.to_csv('Metadata/ReportFoundList.csv',index=False)