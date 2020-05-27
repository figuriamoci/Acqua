from bs4 import BeautifulSoup
import pandas as pd,requests,re
import acqua.aqueduct as aq
url = 'http://www.sisamspa.it/index.php?option=com_content&view=article&id=153:qualita-dell-acqua&catid=28&showall=&limitstart=1'
gestore = "SISAMMantova"
aq.setEnv('Lombardia//'+gestore)
site = 'http://www.sisamspa.it/'
#
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
label = 'PERIODO :'
data_report = soup.body.findAll(text=re.compile(label))[0].split(label)[1].strip()
locationList = pd.read_csv('Metadata/LocationList.csv')
reportFoundList = pd.DataFrame()
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    rete = location['acquedotto']
    urlReport = site+soup.find(text=rete).parent.parent['href']
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report,'urlReport':urlReport}
    reportFoundList = reportFoundList.append( row, ignore_index=True )
#
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)

