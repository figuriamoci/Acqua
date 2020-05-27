##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "SSISPAVercelli"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.siispa.it/qualita-acqua/laboratorio-analisi/qualita-dell-acqua-fornita'
site = 'https://www.siispa.it'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#
div = soup.find("div", {"class": "sppb-article-introtext"})
anchors = div.findAll("a")
alias_city = [a.text.strip() for a in anchors]
alias_address = ["Comune" for c in anchors]
urlReport = [site+a['href'] for a in anchors]
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport})
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)