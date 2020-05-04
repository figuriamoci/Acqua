###
from selenium import webdriver
import pandas as pd
import acqua.aqueduct as aq
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
##Lettura tabella del comune di Alessadria
analisiAlessandriaWebElement = driver.find_element_by_id("gamagc_analisi_alessandria")
rawTable = analisiAlessandriaWebElement.find_element_by_tag_name( "table" )
tableHtml = rawTable.get_attribute( 'outerHTML' )
table = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
locations = table.iloc[:,0]
alias_address = []
for i,loc in enumerate(locations):
    if i>=2: alias_address.extend([l.strip() for l in loc.split("-") ])
locationListAlessandria = pd.DataFrame({'alias_address':alias_address})
locationListAlessandria['alias_city'] = "Alessandria"
locationListAlessandria['georeferencingString'] = locationListAlessandria['alias_address']+", Alessandria, AL, Piemonte"
locationListAlessandria['type'] = 'POINT'
##Lettura tabella di altri comuni della provincia
analisiAltriComuniWebElement = driver.find_element_by_id("gamagc_analisi_altri_comuni")
rawTable = analisiAltriComuniWebElement.find_element_by_tag_name( "table" )
tableHtml = rawTable.get_attribute( 'outerHTML' )
table = pd.read_html( tableHtml, decimal=',', thousands='.' )[0]
locations = table.iloc[:,0]
alias_city = [l.strip() for i,l in enumerate(locations) if i>=2]
locationListAltriComuni = pd.DataFrame({'alias_city':alias_city})
locationListAltriComuni['alias_address'] = "Comune"
locationListAltriComuni['georeferencingString'] = locationListAltriComuni['alias_city']+", AL, Piemonte"
locationListAltriComuni['type'] = 'POINT'
##Concatenate
frames = [locationListAlessandria,locationListAltriComuni]
locationList = pd.concat(frames,sort=False)
locationList.to_csv('Metadata/LocationList.csv',index=False)
