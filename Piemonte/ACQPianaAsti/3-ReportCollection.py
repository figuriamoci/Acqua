##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "ACQPianaAsti"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.acquedottopiana.it/l-acqua'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
site = 'https://www.acquedottopiana.it'
rows = soup.findAll("span", {"class": "name"})
anchors = [r.find("a") for r in rows]
alias_city = [a.text for a in anchors]
alias_address = ['Comune' for a in alias_city]
urlReport = [site+a['href'] for a in anchors]
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport})
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)