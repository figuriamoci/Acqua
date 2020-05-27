##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "SISIAcqueAlba"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.sisiacque.it/?page_id=4117'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
div = soup.find("div", {"id": "main"})
anchors = div.findAll("a")
alias_city = [a.text.replace('Analisi','').strip() for a in anchors if 'Analisi' in a.text]
alias_address = ["Comune" for c in alias_city]
urlReport = [a['href'] for a in anchors if 'Analisi' in a.text]
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport})
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)