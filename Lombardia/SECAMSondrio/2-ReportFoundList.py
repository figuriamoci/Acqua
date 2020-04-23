##
from bs4 import BeautifulSoup
import requests
import pandas as pd,logging
import acqua.aqueduct as aq
id_gestore = "SECAMSondrio"
aq.setEnv('Lombardia//'+id_gestore)
url = 'http://www.secam.net/2013-05-07-13-46-30/servizio-idrico-integrato/le-analisi-dell-acqua.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
tableHtml = soup.find('table')
table = pd.read_html( str(tableHtml))[0]
#
prefix = 'http://www.secam.net'
anchors = tableHtml.findAll("a")
urlReports = [prefix+url.attrs['href'] for url in anchors]
#
#alias_address = [url.contents[0] for url in anchors]
table[3] = urlReports
reportFoundList = table.rename(columns = {0:'alias_city', 1:'alias_address', 3:'urlReport'})
reportFoundList.to_csv('Metadata/DataReportCollection.csv',index=False)
