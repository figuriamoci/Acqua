import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://www.acqualodigiana.it/acqua-del-rubinetto/'
page = requests.get(url)
page.status_code
#page.text
soup = BeautifulSoup(page.text, 'html.parser')
puntiErogazione = ["Abbadia Cerreto","Bertonico", "Boffalora d'Adda", "Borghetto Lodigiano", "Borgo San Giovanni", "Brembio", "Castelgerundo (Fraz. Camairago)", "Casaletto Lodigiano", "Casalmaiocco", "Casalpusterlengo", "Caselle Landi", "Caselle Lurani", "Castelnuovo Bocca d'Adda", "Castiglione d'Adda", "Castiraga Vidardo", "Castelgerundo (Fraz. Cavacurta)", "Cavenago d'Adda", "Cervignano d'Adda", "Codogno", "Comazzo", "Cornegliano Laudense", "Corno Giovine", "Cornovecchio", "Corte Palasio", "Crespiatica", "Fombio", "Galgagnano", "Graffignana", "Guardamiglio", "Livraga", "Lodi", "Lodi Vecchio", "Maccastorna", "Mairago", "Maleo", "Marudo", "Massalengo", "Meleti", "Merlino", "Montanaso Lombardo", "Mulazzano", "Orio Litta", "Ospedaletto Lodigiano", "Ossago Lodigiano", "Pieve Fissiraga", "Salerano sul Lambro", "San Fiorano", "San Martino in Strada", "San Rocco al Porto", "Sant'Angelo Lodigiano", "Santo Stefano Lodigiano", "Secugnago", "Senna Lodigiana", "Somaglia","Sordio","Tavazzano con Villavesco","Terranova dei Passerini","Turano Lodigiano","Valera Fratta","Villanova del Sillaro","Zelo Buon Persico"]
#puntiErogazione = ['Abbadia Cerreto','Bertonico']
                   
#link = open("D:/EmporioADV/acqua-del-rubinetto.xml","r")
#soup = BeautifulSoup(link.read(), 'html.parser')
#link.close()
etichettaPrimaLocalita = soup.find(string=puntiErogazione[0])
tbl = etichettaPrimaLocalita.findNext("table") 
data_frame = pd.read_html(str(tbl),decimal=',',thousands=',',index_col=0,header=0)[0] 
etichetteLodigiane = pd.DataFrame(index=puntiErogazione,columns=data_frame.index)

for localita in puntiErogazione:
    table = soup.find(string=localita)
    tbl = table.findNext("table") 
    data_frame = pd.read_html(str(tbl),decimal=',',thousands=',',index_col=0,header=0)[0]
    row=pd.Series(index=data_frame.index,data=data_frame['Valori'].values)
    etichetteLodigiane.loc[localita]=row

etichetteLodigiane
    
#puntoErog = puntiErogazione[0]
#data_frame.columns
#data_frame.index
#data_frame.columns
#etichette = pd.DataFrame(columns=data_frame.index)
#etichette
#listeEtichette = pd.Series([])
#listeEtichette.append(data_frame)
#listeEtichette.append(data_frame)
#etichette = pd.DataFrame(index=puntiErogazione, columns=data_frame)





#print(soup.prettify())

#table = soup.find(string="Abbadia Cerreto").parent.parent
#lista = table.find_all("tr")
#lista[1]
#for tr in lista:
    #print(tr.findNext("td").findNext("span").get_text())
    #print(tr.findNext("td").findNext("td").get_text())
    #print(tr.findNext("td").findNext("td").findNext("td").get_text())
#    tr.strip()
