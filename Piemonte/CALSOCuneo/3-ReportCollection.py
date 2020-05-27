##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "CALSOCuneo"
aq.setEnv('Piemonte//'+gestore)
url = 'https://calso.org/qualita-e-risorse/analisi-delle-acque/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
anchors = soup.findAll("a", {"class": "heading-link"})
alias_city = [a.text.strip() for a in anchors]
alias_address = ['Comune' for a in alias_city]
urlReport = [a['href'] for a in anchors]
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport})
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)