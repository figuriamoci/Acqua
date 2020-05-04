###
from selenium import webdriver
import pandas as pd
import acqua.aqueduct as aq
import acqua.parametri as parm
import logging,re
gestore = "AMAGAlessandria"
aq.setEnv('Piemonte//'+gestore)
url = 'http://www.gruppoamag.it/laboratorio-analisi/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
useThisDictionary = parm.crea_dizionario('Metadata/SynParametri.csv')
parametersAdmitted = parm.getParametersAdmitted('Metadata/SynParametri.csv')
#Lettura tabella del comune di Alessadria
analisiAlessandriaWebElement = driver.find_element_by_id("gamagc_analisi_alessandria")
rawTable = analisiAlessandriaWebElement.find_element_by_tag_name( "table" )
tableHtml = rawTable.get_attribute( 'outerHTML' ).replace('.',',') #
#Ricerca la data del report
premessa = analisiAlessandriaWebElement.find_element_by_xpath("//*[contains(text(), 'Ultima Modifica:')]").get_attribute( 'outerHTML' )
data_report_Alessandria = re.search("\d\d/\d\d/\d\d\d\d", premessa).group()
table = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
table.columns = table.loc[0]
tableAlessandria = table.copy()
#Lettura tabella altri comuni della provincia di Alessadria
analisiAltriComunuWebElement = driver.find_element_by_id("gamagc_analisi_altri_comuni")
rawTable = analisiAltriComunuWebElement.find_element_by_tag_name( "table" )
tableHtml = rawTable.get_attribute( 'outerHTML' ).replace('.',',')
#Ricerca la data del report
premessa = analisiAltriComunuWebElement.find_element_by_xpath("//*[contains(text(), 'Ultima Modifica:')]").get_attribute( 'outerHTML' )
data_report_AltriComuni = re.search("\d\d/\d\d/\d\d\d\d", premessa).group()
table = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
table.columns = table.loc[0]
tableAltriComuni = table.copy()
report = pd.concat([tableAlessandria,tableAltriComuni],sort=False)
#
locationList = pd.read_csv('Metadata/LocationList.csv')
dataReportCollection = pd.DataFrame()
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    citta = alias_city if alias_address=="Comune" else alias_address
    citta = citta.replace('(', '\(').replace(')', '\)')
    parms_ = report[report['Città'].str.contains(citta)]
    parms = parms_.drop('Città',axis=1).to_dict(orient="record")[0]
    stdParms = parm.standardize( useThisDictionary, parms)
    data_report = data_report_Alessandria if alias_city=='Alessandria' else data_report_AltriComuni
    row = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
    row.update( stdParms )
    dataReportCollection = dataReportCollection.append( row, ignore_index=True )
    logging.info( "Hacked %s/%s (%s/%s)!", alias_city, alias_address, i + 1, len( locationList ) )
#
dataReportCollection.to_csv('Metadata/DataReportCollection.csv',index=False)
