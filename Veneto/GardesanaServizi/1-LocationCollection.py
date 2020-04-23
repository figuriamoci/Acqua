##
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime,logging,requests
import acqua.aqueduct as aq
aq.setEnv('Veneto//GardesanaServizi')
site = 'http://www.ags.vr.it/'
url = "http://www.ags.vr.it/qualita_acqua_analisi_acque.asp"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

listRowTable = soup.findAll("td", {"class": "tdh20 manina"})
a = listRowTable[0]
site+a.get('onclick').replace('location.href=','').replace("'",'')

table = soup.find("table", {"class": "txtb11"})
comuni = table.findAll("a")
alias_city = [city.text for city in comuni]

locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = 'Comune'
locationList['georeferencingString'] = locationList['alias_city'] + ', Verona, Veneto, Italia'
locationList.to_csv('Medadata/LocationList.csv',index=False)
logging.info('Finish: %s',datetime.datetime.now())