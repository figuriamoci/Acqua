##
import pandas as pd
import datetime
import os
import logging
#Inizializzaizone ambiente
logging.basicConfig(level=logging.INFO)
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/AceGasAmga')
url = 'http://www.acegasapsamga.it/binary/hera_acegas/qualita_acqua_trieste/2019_11_novembre_TS.1577977068.pdf'
#Inizio algoritmo
df = pd.read_csv('Definitions/LocationList.csv')
reportList = df.reindex(columns=['alias_city','alias_address'])
reportList['url']=url
reportList.to_csv('Medadata/DataReportCollection.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())
logging.info('Report found: %s',len(reportList))

