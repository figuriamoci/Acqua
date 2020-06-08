##
from bs4 import BeautifulSoup
import pandas as pd,requests,logging
import acqua.aqueduct as aq
gestore = "AGSRiva"
aq.setEnv('Trentino//'+gestore)
url = 'https://www.altogardaservizi.com/acqua-fognatura/qualita-servizio'
##
locationList = pd.read_csv('Metadata/LocationList.csv')
alias_address = locationList['alias_address']
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
divAddressList = soup.find('div',{'class':'download-box'})
urlReport = [divAddressList.find("div",string=address).parent['href'] for address in alias_address]
#
reportFoundList = locationList.copy()
reportFoundList['urlReport']=urlReport
reportFoundList.to_csv('Metadata/ReportFoundList.csv',index=False)
