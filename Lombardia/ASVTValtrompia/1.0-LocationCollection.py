##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging,pandas as pd
import acqua.aqueduct as aq
gestore = "ASVTValtrompia"
aq.setEnv('Lombardia//'+gestore)
puntoDiMonitoraggio = 'https://qualitaacqua.a2acicloidrico.eu/QualitaH2oWeb/resources/images/punti-2.png'
elencoCumuniBrescia = ['Brescia','Desenzano del Garda','Montichiari','Lumezzane','Palazzolo sull''Oglio','Rovato','Chiari','Ghedi','Gussago','Lonato del Garda','Concesio','Darfo Boario Terme','Ospitaletto','Leno','Travagliato','Rezzato','Sarezzo','Manerbio','Carpenedolo','Calcinato','Bagnolo Mella','Orzinuovi','Bedizzole','Mazzano','Gavardo','Gardone Val Trompia','Castenedolo','Castel Mella','Villa Carcina','Cazzago San Martino','Nave','Botticino','Salò','Rodengo Saiano','Roncadelle','Capriolo','Borgosatollo','Iseo','Flero','Coccaglio','Erbusco','Calvisano','Castegnato','Sirmione','Verolanuova','Vobarno','Toscolano-Maderno','Pisogne','Cologne','Bovezzo','Provaglio d''Iseo','Corte Franca','Adro','Castrezzato','Pontevico','Passirano','Prevalle','Pontoglio','Castelcovati','Torbole Casaglia','Quinzano d''Oglio','Villanuova sul Clisi','Rudiano','Dello','Borgo San Giacomo','Trenzano','Manerba del Garda','Esine','Poncarale','Gottolengo','Montirone','Cellatica','Breno','Roccafranca','Gambara','Nuvolera','Paratico','San Zeno Naviglio','Pian Camuno','Piancogno','Capriano del Colle','Collebeato','Edolo','Roè Volciano','San Paolo','Padenghe sul Garda','Monticelli Brusati','Vestone','Marcheno','Offlaga','Isorella','Nuvolento','Sabbio Chiese','Bagolino','Comezzano-Cizzago','Lograto','Pompiano','Urago d''Oglio','Verolavecchia','Paderno Franciacorta','Artogne','Calvagese della Riviera','Pozzolengo','Bienno','Mairano','San Felice del Benaco','Puegnago sul Garda','Sale Marasino','Remedello','Marone','Malonno','Azzano Mella','Ome','Serle','Pralboino','Gargnano','Pavone del Mella','Cividate Camuno','Berlingo','Gardone Riviera','Muscoline','Polpenazze del Garda','Borno','San Gervasio Bresciano','Moniga del Garda','Polaveno','Alfianello','Berzo Inferiore','Orzivecchi','Capo di Ponte','Angolo Terme','Barbariga','Bassano Bresciano','Bovegno','Caino','Gianico','Collio','Paitone','Tremosine sul Garda','Fiesse','Malegno','Niardo','Visano','Odolo','Idro','Corteno Golgi','Sulzano','Ceto','Soiano del Lago','Milzano','Agnosine','Monte Isola','Ponte di Legno','Casto','Brandico','Lodrino','Berzo Demo','Cigole','Acquafredda','Preseglie','Pezzaze','Maclodio','Sellero','Vezza d''Oglio','Seniga','Ossimo','Villachiara','Corzano','Vallio Terme','Bione','Tavernole sul Mella','Sonico','Tignale','Cedegolo','Barghe','Limone sul Garda','Temù','Zone','Ono San Pietro','Provaglio Val Sabbia','Saviore dell''Adamello','Cevo','Mura','Brione','Braone','Vione','Cerveno','Marmentino','Pertica Bassa','Paspardo','Losine','Longhena','Pertica Alta','Cimbergo','Monno','Lavenone','Treviso Bresciano','Anfo','Lozio','Incudine','Capovalle','Valvestino','Paisco Loveno','Magasa','Irma']
#
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 20 )  # seconds
driver.get( "https://qualitaacqua.asvt-spa.it/QualitaH2oWeb/" )
time.sleep(10)
###
locationList = pd.DataFrame()
for i,comune in enumerate(elencoCumuniBrescia):
    try:
        driver.get( "https://qualitaacqua.asvt-spa.it/QualitaH2oWeb/" )
        time.sleep( 10 )
        #i=73
        #comune = elencoCumuniBrescia[i]
        logging.info("Processing %s... (%s/%s)",comune,i+1,len(elencoCumuniBrescia))
        input = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_id( "autocomplete" ) ) )
        input.clear()
        input.send_keys(comune+", BS, Lombardia")
        input.send_keys(Keys.ENTER)
        time.sleep(5)
        div = WebDriverWait( driver, 20 ).until( EC.visibility_of( driver.find_element_by_css_selector( "#map-canvas > div > div > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(3)" ) ) )
        WebDriverWait(div, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "div")))
        listDiv = div.find_elements_by_tag_name("div")
        addressList = []
        for a in listDiv:
            location = a.get_attribute( "title" )
            location = location.replace('-',':')
            if location!= "":
                try:
                    alias_city = location.split(":")[0].strip()
                    alias_address = location.split(":")[1].split("-")[0].strip()
                    georeferencingString = alias_address+", "+alias_city+", BS, Lombardia, Italia"
                    element = {'location':location, 'alias_city': alias_city, 'alias_address':alias_address, 'georeferencingString':georeferencingString, 'type':'POINT'  }
                    addressList.append(element)
                except:
                    logging.info( "Passed address %s for %s.", location, comune)
        if len(addressList)>0:
            locationList = locationList.append(addressList,ignore_index=True)
            logging.info( "Hacked %s!. Add %s address.", comune , len(addressList))
    except:
        logging.critical("Skiped %s! [i=%s] ",comune,i)

driver.close()
##
#tableWebElement = driver.find_element_by_id("parameters")
#tableHtml = tableWebElement.get_attribute('outerHTML')
#table = pd.read_html(tableHtml,decimal=',',thousands='.')[0]
locationList.to_csv('Metadata/LocationList.csv',index=False)


