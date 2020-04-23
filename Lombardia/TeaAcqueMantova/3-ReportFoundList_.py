##
from bs4 import BeautifulSoup
import pandas as pd,requests,io
import acqua.aqueduct as aq
gestore = "TeaAcqueMantova"
aq.setEnv('Lombardia//'+gestore)
url = 'https://www.cometea.it/verifica-la-tua-acqua/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
map = soup.findAll("area", {"shape": "poly"})
comuniList = [comune['href'].split('/') for comune in list(map)]
alias_city = [comune[len(comune)-1].replace('-',' ') for comune in comuniList]
urlReport = [comune['href'] for comune in list(map)]
##
reportFoundList = pd.DataFrame({'alias_city':alias_city,'urlReport':urlReport})
reportFoundList['alias_address'] = 'Comune'
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)
