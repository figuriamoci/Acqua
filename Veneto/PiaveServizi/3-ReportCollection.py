##
from bs4 import BeautifulSoup
import pandas as pd,requests,re
import acqua.aqueduct as aq
gestore = "PiaveServizi"
aq.setEnv('Veneto//'+gestore)
url = 'https://www.piaveservizi.eu/home/Acqua/Qualita.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
site = 'https://www.piaveservizi.eu'
aqueductList_ = pd.read_csv('Metadata/AqueductList.csv').groupby('acquedotto').count()
aqueductList_.reset_index(inplace=True)
aqueductList = list(aqueductList_['acquedotto'])
##
urlReportDict = {}
for i in range(0,len(aqueductList)):
    aqueduct = aqueductList[i]
    urlReport = site+soup.find( 'a', href=True, text=re.compile(aqueduct) )['href']
    urlReportDict.update({aqueduct:urlReport})
##
reportFoundList = pd.read_csv('Metadata/AqueductList.csv')
reportFoundList['urlReport'] = reportFoundList['acquedotto'].apply(lambda a:urlReportDict[a])
reportFoundList.to_csv("Metadata/ReportFoundList.csv",index=False)