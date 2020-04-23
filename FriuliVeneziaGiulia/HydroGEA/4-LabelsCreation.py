##
import acqua.label as al
import acqua.labelCollection as coll
import acqua.parametri as parm
import pandas as pd
import logging
import acqua.aqueduct as aq
cod_gestore = "HydroGEA"
aq.setEnv('FriuliVeneziaGiulia//'+cod_gestore)
parm.crea_dizionario('Medadata/SynParametri.csv')
useThisDictionary = parm.crea_dizionario('Medadata/SynParametri.csv')
##
def get_rawTable(url_report):
    import tabula
    row_table = tabula.read_pdf(url_report, stream=True,pages="all")
    row_table2 = row_table.T.reset_index().T
    return row_table2

def estractLabelFromRawTable(address,rawTable):
    import numpy as np
    parms = ['ph', 'Residuo fisso a 180°', 'Resid. fisso 180°', 'Durezza', 'Conducibilità', 'Calcio', 'Magnesio',
             'Ammonio', 'Cloruri',
             'Solfati', 'Potassio', 'Sodio', 'Arsenico', 'Bicarbonato', 'Cloro residuo', 'Fluoruri', 'Nitrati',
             'Nitriti',
             'Manganese']
    #parametersAdmitted = parm.getParametersAdmitted( 'Medadata/SynParametri.csv' )
    table_ = rawTable.reset_index()
    boolMatrix = table_.apply(lambda x: x.str.contains(address, na=False))
    alias_coordinates_ = np.where(boolMatrix)
    if len(alias_coordinates_[0])==0 or len(alias_coordinates_[1])==0: raise AddressNotFound("%s not found.",address)
    alias_coordinates = [x[0] for x in alias_coordinates_]
    alias_address = table_.iloc[alias_coordinates]
    rowFound = alias_coordinates[0]
    columnFound = alias_coordinates[1]
    table_.set_index(0,inplace=True)
    label = table_.reindex(index=parms,columns=[columnFound-1])
    label_cleaned = label.dropna()
    label_cleaned.columns = ['label']
    lbdict = label_cleaned['label'].to_dict()
    #
    data_report = table_.reindex(index=['Data del prelievo'],columns=[columnFound-1]).iloc[0]
    #
    ll = {}
    ll['alias_address'] = address
    ll['data_report'] = data_report[columnFound-1]
    ll['label'] = lbdict
    return ll

reportFoundList = pd.read_csv( 'Definitions/ReportFoundList.csv' )
#reportFoundList = reportFoundList.iloc[82:]
logging.info('Caricato la DataReportCollection.csv con %s elementi.',len(reportFoundList))
##
ll = []
for i,location in reportFoundList.iterrows():
    address = location['alias_address']
    city = location['alias_city']
    urlReport_ = location['urlReport']
    urlReport = urlReport_.replace('%20',' ')
    rawTable = get_rawTable(urlReport)
    try:
        rawLabel = estractLabelFromRawTable(address,rawTable)
        label = rawLabel['label']
        data_report = rawLabel['data_report']
        lb = al.create_label(useThisDictionary,cod_gestore,data_report,label)
        glb = al.addGeocodeData(lb,(city,address),'Medadata/GeoReferencedLocationsList.csv')
        ll.extend( glb )
        logging.info( 'Hacked %s/%s (Progress %s/%s)', city, address, i, len( reportFoundList ) - 1 )
    except:
        logging.critical('Skip label for %s/%s',city, address)

##
import pickle
with open('filename.pickle', 'wb') as handle: pickle.dump(ll, handle)

fc = coll.to_geojson(ll)
coll.to_file(fc,cod_gestore+'.geojson')
coll.display(fc)

logging.info('Created %s label(s) of %s.',len(ll),len(reportFoundList))
logging.info('End process.')
