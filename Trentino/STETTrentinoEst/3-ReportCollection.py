##
from bs4 import BeautifulSoup
import pandas as pd,requests,logging
import acqua.aqueduct as aq
gestore = "STETTrentinoEst"
aq.setEnv('Trentino//'+gestore)
site = 'https://www.stetspa.it'
#
locationList = pd.read_csv('Metadata/LocationList.csv')
#urlPageList = locationList.groupby('aqueduct').first()['urlPage']
reportFoundList = pd.DataFrame()
for i,loc in locationList.iterrows():
    #aqueduct = 'Assizzi, Masetti'
    #urlPage = urlPageList[aqueduct]
    alias_city = loc['alias_city']
    alias_address = loc['alias_address']
    aqueduct = loc['aqueduct']
    urlPage = loc['urlPage']
    logging.info('Reading %s/%s (%s/%s).',alias_city,alias_address,i,len(locationList))
    #
    page = requests.get(urlPage)
    soup = BeautifulSoup(page.text, 'html.parser')
    urlReportPage = site+soup.find("a", string=aqueduct)['href']
    #
    page = requests.get(urlReportPage)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        rawReportLink = soup.find( 'span', {'class': 'file'} )
        anchor = rawReportLink.find('a')
        urlReport = anchor['href']
        data_report = anchor.text
        row = {'alias_city':alias_city,'alias_address':alias_address,'aqueduct':aqueduct,'urlReport':urlReport,'data_report':data_report}
        reportFoundList = reportFoundList.append( row, ignore_index=True )
    except:
        logging.critical('Skiped %s/%s.',alias_city,alias_address)

#
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)