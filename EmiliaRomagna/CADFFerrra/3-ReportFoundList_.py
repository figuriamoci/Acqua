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
alias_address = ["Comune" for l in locations]
urlReport = [l['href'] for l in locations]
##
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport})
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)
