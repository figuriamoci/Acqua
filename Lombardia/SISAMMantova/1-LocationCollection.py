from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
url = 'http://www.sisamspa.it/index.php?option=com_content&view=article&id=153:qualita-dell-acqua&catid=28&showall=&limitstart=1'
gestore = "SISAMMantova"
aq.setEnv('Lombardia//'+gestore)
#
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table')
cellList = table.find_all('td')
acquedotti = [cell.text for cell in cellList if 'Rete di' in cell.text]
alias_city = [a.replace('Rete di ','') for a in acquedotti]
locationList = pd.DataFrame({'alias_city':alias_city,'acquedotto':acquedotti})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", MN"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)

