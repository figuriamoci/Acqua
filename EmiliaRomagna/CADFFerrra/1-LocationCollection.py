from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "CADFFerrra"
aq.setEnv('EmiliaRomagna//'+gestore)
url = 'http://www.cadf.it/qualita-acqua'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
container = soup.select("div.panes:nth-child(5) > div:nth-child(1) > ul:nth-child(3)")[0]
locations = container.findAll("a")
alias_city = [l.text for l in locations]
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", Ferrara, Emilia Romagna"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
