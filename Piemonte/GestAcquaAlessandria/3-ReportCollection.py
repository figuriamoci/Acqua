##
from bs4 import BeautifulSoup
import pandas as pd,requests
import acqua.aqueduct as aq
gestore = "GestAcquaAlessandria"
aq.setEnv('Piemonte//'+gestore)
url = 'https://www.gestioneacqua.it/servizi/qualita-dellacqua/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
div = soup.select("section.elementor-element:nth-child(3) > div:nth-child(1) > div:nth-child(1)")[0]
anchors = div.findAll("a")
alias_city = [a.get_text().strip() for a in anchors]
alias_address = ['Comune' for a in alias_city]
urlReport = [a['href'] for a in anchors]
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport})
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)