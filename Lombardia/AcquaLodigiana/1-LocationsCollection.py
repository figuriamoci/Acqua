#%%
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd,datetime,os,logging
#os.chdir('D://Python//Acqua')
os.chdir('//Users//andrea//PycharmProjects//Acqua')
os.chdir('Lombardia//AcquaLodigiana')
logging.basicConfig(level=logging.INFO)
##
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.get('http://www.acqualodigiana.it/acqua-del-rubinetto/')
#######################################
#Sono fornite le località oggetto delle analisi, raccolte dalle pagine web
listLocAdmitted = ["Abbadia Cerreto","Bertonico", "Boffalora d'Adda", "Borghetto Lodigiano", "Borgo San Giovanni", "Brembio", "Castelgerundo (Fraz. Camairago)", "Casaletto Lodigiano", "Casalmaiocco", "Casalpusterlengo", "Caselle Landi", "Caselle Lurani", "Castelnuovo Bocca d'Adda", "Castiglione d'Adda", "Castiraga Vidardo", "Castelgerundo (Fraz. Cavacurta)", "Cavenago d'Adda", "Cervignano d'Adda", "Codogno", "Comazzo", "Cornegliano Laudense", "Corno Giovine", "Cornovecchio", "Corte Palasio", "Crespiatica", "Fombio", "Galgagnano", "Graffignana", "Guardamiglio", "Livraga", "Lodi", "Lodi Vecchio", "Maccastorna", "Mairago", "Maleo", "Marudo", "Massalengo", "Meleti", "Merlino", "Montanaso Lombardo", "Mulazzano", "Orio Litta", "Ospedaletto Lodigiano", "Ossago Lodigiano", "Pieve Fissiraga", "Salerano sul Lambro", "San Fiorano", "San Martino in Strada", "San Rocco al Porto", "Sant'Angelo Lodigiano", "Santo Stefano Lodigiano", "Secugnago", "Senna Lodigiana", "Somaglia","Sordio","Tavazzano con Villavesco","Terranova dei Passerini","Turano Lodigiano","Valera Fratta","Villanova del Sillaro","Zelo Buon Persico"]
soup = BeautifulSoup(driver.page_source, 'html.parser')
listHtmlComuni = list(soup.findAll("div", {"class": "su-spoiler-title"}))
#%%
alias_city = []
for i,lochtml in enumerate(listHtmlComuni):
    loc = lochtml.get_text()
    if loc in listLocAdmitted:
        alias_city.append(loc)
    else:
        logging.critical(">>> %s is skipped",loc)
#%%
driver.close()
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = 'Territorio'
locationList['georeferencingString'] = locationList['alias_city']+' , Lodi, Lombardia, Italia'
locationList['type'] = 'POINT'
locationList.to_csv('Definitions/LocationList.csv',index=False)
