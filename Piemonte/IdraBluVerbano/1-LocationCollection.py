from selenium import webdriver
import logging,pandas as pd
import acqua.aqueduct as aq
import warnings,io,pdfquery,requests,tabula
gestore = "IdraBluVerbano"
aq.setEnv('Piemonte//'+gestore)
url = 'http://www.idrablu.it/qualita-e-sicurezza-dellacqua/'
warnings.simplefilter(action='ignore', category=FutureWarning)
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
alias_city = list(table.iloc[2:len(table)-1,0])
locationList = pd.DataFrame({"alias_city":alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", VB, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
