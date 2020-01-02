import camelot
import wl.Classes.Label as lb
import wl.Classes.LabelsCollection as lbc
import wl.Classes.GeoPointLabel as gpl

idGestore = 7396
gestoreAcqua = 'IRISACQUA SRL'
sito_internet = 'http://www.irisacqua.it'
url = "http://www.irisacqua.it/ProxyVFS.axd/null/r22231/Analisi-acqua-I-semestre-2019-pdf?ext=.pdf"

######################
LocationlistAlias = ["Isola Morosini","Gorizia","Farra","Cormons","Dolegna","Monfalcone","Ronchi dei Legionari","Grado","San Pier d'Isonzo"]
dataReport='ANALISI ACQUA - ANNO 2019 I SEMESTRE'

tables = camelot.read_pdf(url)
print(tables[0].parsing_report)
row_table = tables[0].df

locationAlias = row_table.iloc[0,3:]
locationAlias = locationAlias.apply(lambda x:x.replace('\n',''))
cleaned_table = row_table.drop([0,1],axis=0) #Rimosse due righe
cleaned_table = cleaned_table.drop([1,2],axis=1) #Rimosse 1 riga
cleaned_table = cleaned_table.set_index(0)
cleaned_table.columns = locationAlias #colonne impostate con i parametri

print(locationAlias)

from wl.Classes import Label,LabelsCollection,GeoPointLabel
c = lbc.LabelsCollection([])

for alias in LocationlistAlias:
    etichetta = lb.Label(idGestore,alias,dataReport,cleaned_table[alias].to_dict())
    # Applica i dati Geo
    geoEtichetta = gpl.GeoPointLabel(etichetta)
    #collect list smlabel
    c.append(geoEtichetta)

c.display()