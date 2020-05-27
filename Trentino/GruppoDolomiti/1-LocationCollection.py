#
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import acqua.aqueduct as aq
gestore = "GruppoDolomiti"
aq.setEnv('Trentino//'+gestore)
#url = 'https://www.gruppodolomitienergia.it/content/l-acqua-che-beviamo'
url = 'https://www.gruppodolomitienergia.it/content/mappa-di-trento'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 10 )  # seconds
driver.get( url )
marker = 'http://www.gruppodolomitienergia.it/upload/ent3/1/icon_water.png'
#
mapWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "map_canvas" ) ) )
markersWebElement = [m for m in mapWebElement.find_elements_by_tag_name('img') if m.get_attribute('src')==marker]
divCells = [m.find_element_by_xpath("..") for m in markersWebElement]
locations = [d.get_attribute('title').strip()  for d in divCells if d.get_attribute('title').strip() != '' ]
alias_city = [l.split('-')[0].strip() for l in locations]
alias_address = [l.strip() for l in locations]
#
locationList_ = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address})
locationList = locationList_.groupby(['alias_city','alias_address']).count() #Toglie gli alias duplicati
locationList.reset_index(inplace=True)
locationList['georeferencingString'] = locationList['alias_address']+", TN"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)

