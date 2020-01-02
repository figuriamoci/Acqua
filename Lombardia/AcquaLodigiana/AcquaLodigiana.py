import requests
from bs4 import BeautifulSoup
import pandas as pd

import wl.Classes.Label as lb
import wl.Classes.LabelsCollection as lbc
import wl.Classes.GeoPointLabel as gpl

#Prende in input la pagina web dei dati delle analisi
url = 'http://www.acqualodigiana.it/acqua-del-rubinetto/'
idGestore = 16779
gestoreAcqua = 'SOCIETA'' ACQUA LODIGIANA SRL'
sito_internet = 'http://www.acqualodigiana.it'
dataReport = '2018'

#######################################
#Sono fornitoi le località oggettodelle analisi, raccolte dalle pagine web
listAliasLocalition = ["Abbadia Cerreto","Bertonico", "Boffalora d'Adda", "Borghetto Lodigiano", "Borgo San Giovanni", "Brembio", "Castelgerundo (Fraz. Camairago)", "Casaletto Lodigiano", "Casalmaiocco", "Casalpusterlengo", "Caselle Landi", "Caselle Lurani", "Castelnuovo Bocca d'Adda", "Castiglione d'Adda", "Castiraga Vidardo", "Castelgerundo (Fraz. Cavacurta)", "Cavenago d'Adda", "Cervignano d'Adda", "Codogno", "Comazzo", "Cornegliano Laudense", "Corno Giovine", "Cornovecchio", "Corte Palasio", "Crespiatica", "Fombio", "Galgagnano", "Graffignana", "Guardamiglio", "Livraga", "Lodi", "Lodi Vecchio", "Maccastorna", "Mairago", "Maleo", "Marudo", "Massalengo", "Meleti", "Merlino", "Montanaso Lombardo", "Mulazzano", "Orio Litta", "Ospedaletto Lodigiano", "Ossago Lodigiano", "Pieve Fissiraga", "Salerano sul Lambro", "San Fiorano", "San Martino in Strada", "San Rocco al Porto", "Sant'Angelo Lodigiano", "Santo Stefano Lodigiano", "Secugnago", "Senna Lodigiana", "Somaglia","Sordio","Tavazzano con Villavesco","Terranova dei Passerini","Turano Lodigiano","Valera Fratta","Villanova del Sillaro","Zelo Buon Persico"]

page = requests.get(url)
page.status_code
soup = BeautifulSoup(page.text, 'html.parser')
#legenda=html_table['Unità di misura']
e = lbc.LabelsCollection([])

for aliasLoc in listAliasLocalition:
    #Find html table refereterd to località
    table = soup.find(string=aliasLoc)
    tbl = table.findNext("table")
    html_table = pd.read_html(str(tbl),decimal=',',thousands=',',index_col=0,header=0)[0]
    #Get labels
    row=pd.Series(index=html_table.index,data=html_table['Valori'].values)
    #Crete smartlabel
    etichetta = lb.Label(16779,aliasLoc,dataReport,row.to_dict())
    # Applica i dati Geo
    geoEtichetta = gpl.GeoPointLabel(etichetta)
    #collect list smlabel
    e.append(geoEtichetta)
    
###############

e.display()

