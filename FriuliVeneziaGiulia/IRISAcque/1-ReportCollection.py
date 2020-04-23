#
import pandas as pd
import datetime,os,logging
#Inizializzazione ambiente
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque')
idGestore = 7396
url = "http://www.irisacqua.it/ProxyVFS.axd/null/r22231/Analisi-acqua-I-semestre-2019-pdf?ext=.pdf"

#Inizio algoritmo
df = pd.read_csv('Definitions/LocationList.csv')
reportList = df.reindex(columns=['alias_city','alias_address'])
reportList['url']=url
reportList_ = reportList.drop_duplicates()
reportList_.to_csv('Medadata/DataReportCollection.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
logging.info('Report found: %s',len(reportList))
