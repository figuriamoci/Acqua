##
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime,logging,requests
import acqua.aqueduct as aq
site = 'http://www.ags.vr.it/'
aq.setEnv('Veneto//GardesanaServizi')
url = "http://www.ags.vr.it/qualita_acqua_analisi_acque.asp"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
#
locationList = pd.read_csv( 'Medadata/LocationList.csv' )
reportFoundList = pd.DataFrame()
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    #
    anchor = soup.findAll("a",text=alias_city)
    urlReport = site + anchor[0]['href']
    row = {'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport}
    reportFoundList = reportFoundList.append(row,ignore_index=True)
##
reportFoundList.to_csv('Medadata/DataReportCollection.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())

