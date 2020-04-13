##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "LarioLecco"
aq.setEnv('Lombardia//'+gestore)
elencoCumuniLecco = ['Abbadia Lariana', 'Airuno', 'Annone Brianza', 'Ballabio', 'Barzago', 'Barzano''', 'Barzio', 'Bellano', 'Bosisio Parini', 'Brivio', 'Bulciago', 'Calco', 'Calolziocorte', 'Carenno', 'Casargo', 'Casatenovo', 'Cassago Brianza', 'Cassina Valsassina', 'Castello Brianza', 'Cernusco Lombardone', 'Cesana Brianza', 'Civate', 'Colico', 'Colle Brianza', 'Cortenova', 'Costa Masnaga', 'Crandola Valsassina', 'Cremella', 'Cremeno', 'Dervio', 'Dolzago', 'Dorio', 'Ello', 'Erve', 'Esino Lario', 'Galbiate', 'Garbagnate Monastero', 'Garlate', 'Imbersago', 'Introbio', 'Lecco', 'Lierna', 'Lomagna', 'Malgrate', 'Mandello del Lario', 'Margno', 'Merate', 'Missaglia', 'Moggio', 'Molteno', 'Monte Marenzo', 'Montevecchia', 'Monticello Brianza', 'Morterone', 'Nibionno', 'Oggiono', 'Olgiate Molgora', 'Olginate', 'Oliveto Lario', 'Osnago', "Paderno d'Adda", 'Pagnona', 'Parlasco', 'Pasturo', 'Perledo', 'Pescate', 'Premana', 'Primaluna', 'Robbiate', 'Rogeno', "Santa Maria Hoe'", 'Sirone', 'Sirtori', 'Sueglio', 'Suello', 'Taceno', 'Valgreghentino', 'Valmadrera', 'Varenna', 'Vercurago', 'Verderio', "Vigano'"]
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
#options.add_argument( '--headless' )
locationList = pd.DataFrame()
##
for i,comune in enumerate(elencoCumuniLecco):
    #i=0
    #comune=elencoCumuniLecco[0]
    logging.info( "Processing %s...",comune)
    driver = webdriver.Chrome( "chromedriver", options=options )
    driver.implicitly_wait( 10 )  # seconds
    driver.get( "http://box.larioreti.it/Box7/#analisi" )
    time.sleep(5)
    inputComune = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#gwt-uid-5 > div > div:nth-child(2) > div > input" ) ) )
    inputComune.send_keys( comune )
    time.sleep(3)
    inputComune = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#gwt-uid-5 > div > div:nth-child(2) > div > input" ) ) )
    inputComune.send_keys( Keys.ENTER )
    time.sleep(2)
    #
    selectIndirizzi = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#gwt-uid-5 > div > div:nth-child(3) > div > div" ) ) )
    driver.execute_script( "arguments[0].click();", selectIndirizzi )
    time.sleep( 2 )
    comuneList = []
    indirizziList = []
    cicli=0
    try:
        while True and cicli<=1000:
            cicli=cicli+1
            logging.info('ciclo %s',cicli)
            tableWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#VAADIN_COMBOBOX_OPTIONLIST > div > div.v-filterselect-suggestmenu > table" ) ) )
            tableHtml = tableWebElement.get_attribute( 'outerHTML' )
            table = pd.read_html( tableHtml)[0]
            indirizziList.extend(list(table[0]))
            comuneList.extend([comune for i in list(table[0])])            #
            next = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#VAADIN_COMBOBOX_OPTIONLIST > div > div.v-filterselect-nextpage > span" ) ) )
            driver.execute_script( "arguments[0].click();", next )
            time.sleep( 1 )
    except:
        logging.info("Hacked %s and %s address! (%s/%s)",comune,len(indirizziList),i+1,len(elencoCumuniLecco))

    row = {'alias_city':comuneList,'alias_address':indirizziList}
    locationList_ = pd.DataFrame(row)
    locationList = locationList.append(locationList_, ignore_index = True)
    driver.close()
#
locationList.to_csv('Metadata/LocationList.csv',index=False)


