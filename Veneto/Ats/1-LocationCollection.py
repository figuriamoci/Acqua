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
locationList = pd.DataFrame()
rowParameters = {}

##
for l in listRowTable:
    title = l['data-title']
    data = l['data-text']

    alias = title.split('-')
    if len(alias)==1:
        alias_city = alias[0].strip()
        alias_address = ''
    else:
        alias_city = alias[1].strip()
        alias_address = alias[0].strip()

    georeferencingString = alias_city+' '+alias_address

    row = {'alias_city':alias_city, 'alias_address':alias_address, 'georeferencingString':georeferencingString}
    locationList = locationList.append(row,ignore_index=True)

    htmltable = pd.read_html(data,decimal=',')[0]
    rowData = {'alias_city': alias_city, 'alias_address': alias_address, 'parameters': htmltable}

    rowParameters.update(rowData)
##

#DataCleaning on georeferencingString...
listRemoveString = ['</strong>','<br />','Zona']
for rs in listRemoveString: locationList['georeferencingString'] = locationList['georeferencingString'].apply(lambda s: s.replace( rs, '' ).strip() )

locationList.to_csv('Medadata/LocationList.csv',index=False)

logging.info('Finish: %s',datetime.datetime.now())