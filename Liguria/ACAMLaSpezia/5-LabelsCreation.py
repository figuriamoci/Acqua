import acqua.aqueduct as aq
import acqua.label as al
import acqua.labelCollection as coll
gestore = "ACAMLaSpezia"
aq.setEnv('Liguria//'+gestore)
dataReportCollectionFile = 'Metadata/DataReportCollection.csv'
geoReferencedLocationsListFile = 'Metadata/GeoReferencedLocationsList.csv'
fc = al.createJSONLabels(gestore,dataReportCollectionFile,geoReferencedLocationsListFile)
coll.display(fc)

import pandas as pd
data = pd.read_csv('Metadata/DataReportCollection.csv')
data.residuo_fisso.min(),data.residuo_fisso.max()

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.plot(data.residuo_fisso)