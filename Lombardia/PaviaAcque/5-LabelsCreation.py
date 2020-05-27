import acqua.aqueduct as aq
import acqua.label as al
import acqua.labelCollection as coll
gestore = "PaviaAcque"
aq.setEnv('Lombardia//'+gestore)
dataReportCollectionFile = 'Metadata/DataReportCollection.csv'
geoReferencedLocationsListFile = 'Metadata/GeoReferencedLocationsList.csv'
fc = al.createJSONLabels(gestore,dataReportCollectionFile,geoReferencedLocationsListFile)
coll.display(fc)

