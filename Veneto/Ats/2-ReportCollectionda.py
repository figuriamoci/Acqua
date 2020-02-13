##
from bs4 import BeautifulSoup
import pandas as pd
import datetime,os,logging,requests

os.chdir('/Users/andrea/PycharmProjects/Acqua/Veneto/Ats')
logging.basicConfig(level=logging.INFO)

url = "https://altotrevigianoservizi.it/reti-e-impianti/acqua-potabile"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

listRowTable = soup.findAll("div", {"class": "col-sm-4 box_dealer boxdistributore hidden"})
##
foundReportList =[]
for l in listRowTable:
    title = l['data-title']
    data = l['data-text']

    alias = title.split('-')
    if len(alias) == 1:
        alias_city = alias[0].strip()
        alias_address = ''
    else:
        alias_city = alias[1].strip()
        alias_address = alias[0].strip()

    htmltable = pd.read_html(data,decimal=',')[0]
    rowData = {'alias_city': alias_city, 'alias_address': alias_address, 'parameters': htmltable}

    foundReportList.append(rowData)
##
import pickle
f = open("Definitions/FoundReportList.pkl","wb")
pickle.dump(foundReportList,f)
f.close()

logging.info('Finish: %s',datetime.datetime.now())