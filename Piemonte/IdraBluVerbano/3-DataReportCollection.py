##Prologo
from selenium import webdriver
import logging,pandas as pd
import acqua.aqueduct as aq
import warnings,io,pdfquery,requests,tabula,re
import acqua.parametri as parm
gestore = "IdraBluVerbano"
aq.setEnv('Piemonte//'+gestore)
url = 'http://www.idrablu.it/qualita-e-sicurezza-dellacqua/'
warnings.simplefilter(action='ignore', category=FutureWarning)
#Caricamento dizionari
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
#Lettura tabella e manipolazione
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
link = driver.find_element_by_partial_link_text("Confronto qualitativo tra l’acqua Idrablu")
urlReport = link.get_attribute("href")
table = tabula.read_pdf(urlReport,stream=True,encoding='utf-8',multiple_tables=True)[0]
table.columns = table.loc[0].str.lower()
table.set_index(table.columns[0],inplace=True)
#La data del report è dedotta dall'URL del report a cui viene aggiunto, per maggiore leggibilità il primo giorno.
premessa = re.search("/\d\d\d\d/\d\d/", urlReport).group()
data_report = premessa+"01"
dataReportCollection = pd.DataFrame()
alias_address = "Comune"
locationList = pd.read_csv('Metadata/LocationList.csv')
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    parms = table.loc[alias_city]
    stdParms = parm.standardize( useThisDictionary, parms.to_dict() )
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( 'Hacked %s/%s (%s/%s)', alias_city, alias_address, i, len( locationList ) - 1 )
##
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
