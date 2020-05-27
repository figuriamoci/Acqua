##
import pandas as pd
from bs4 import BeautifulSoup
import requests
import acqua.aqueduct as aq
url = 'https://www.aimag.it/cosa-facciamo/ciclo-idrico-integrato/controlli-acqua/'
gestore = "AIMAGModena"
aq.setEnv('EmiliaRomagna//'+gestore)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
div = soup.find('div',{'class':'entry-content'})
anchors = div.find_all('a')
urlReportList = [a['href'] for a in anchors]
#
city_acqueduct = pd.read_csv('Metadata/Alias_city.csv')
acqueductList = list(city_acqueduct['acquedotto'].drop_duplicates())
acqueductMap = {acqueduct:[r for r in urlReportList if acqueduct in r][0] for acqueduct in acqueductList}
##
reportFoundList = city_acqueduct
reportFoundList['urlReport'] = reportFoundList['acquedotto'].apply(lambda a: acqueductMap[a] )
reportFoundList['alias_address'] = 'Comune'
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)





##

