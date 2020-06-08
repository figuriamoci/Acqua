##
from bs4 import BeautifulSoup
import pandas as pd,requests,logging
import acqua.aqueduct as aq
gestore = "STETTrentinoEst"
aq.setEnv('Trentino//'+gestore)
url = 'https://www.stetspa.it/attivita/acquedotto/qualita-dellacqua#main-content'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
site = 'https://www.stetspa.it'
#
cityList = ['Pergine Valsugana','Levico Terme','Caldonazzo','Tenna','Borgo Valsugana','Grigno','Albiano','Novaledo']
anchorList = [site+soup.find("a", string=city)['href'] for city in cityList]
df = pd.DataFrame({'city':cityList,'urlPage':anchorList})
locationList = pd.DataFrame()
#
for i,d in df.iterrows():
    city = d['city']
    urlPage = d['urlPage']
    logging.info('Reading addresses for %s',city)
    page = requests.get( urlPage )
    soup = BeautifulSoup( page.text, 'html.parser' )
    rawAqueductTable = soup.find('table',{'class':'views-table'})
    aqueductTable = pd.read_html(str(rawAqueductTable))[0]
    aqueductTable.dropna(axis=0,how='all',inplace=True)
    aqueductTable.dropna(axis=1,how='all',inplace=True)
    aqueductTable.set_index('Acquedotto',inplace=True)
    acquductList = list(aqueductTable.index)
    #
    for aq in acquductList:
        #aq=acquductList[0]
        alias_address_ = list(aqueductTable.loc[aq].str.split(','))[0]
        alias_address = [aa.strip() for aa in alias_address_]
        alias_city = [city for a in alias_address]
        aqueduct = [aq for a in alias_address]
        loc = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'aqueduct':aq,'urlPage':urlPage})
        locationList = locationList.append(loc)
#
locationList['georeferencingString'] = locationList['alias_address']+', '+locationList['alias_city']+", TN, Trentino"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
