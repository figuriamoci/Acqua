import acqua.parametri as sp
import acqua.parametri as par
import pandas as pd
import acqua.aqueduct as aq
import time, geojson,numpy as np,logging,math

def create_label (synonimous,gestore,data_report,parms):
    data = {}
    propGestore = aq.name(gestore)
    data['id_gestore'] = gestore
    data['gestore'] = propGestore['ENTE_GESTORE']
    data['web'] = propGestore['SITO_INTERNET']
    data['report'] = propGestore['URL_QUALITA_ACQUA']
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime( "%d/%m/%Y, %H:%M", named_tuple )
    data['timestamp'] = time_string
    #data['data'] = data_report
    parameters = {sp.getSTDParm(synonimous,k): str(v) for k, v in parms.items()}
    #parameters = {sp.getSTDParm(synonimous,k): str(v).replace(' ','') for k, v in parms.items()}
    data['parameters'] = parameters
    return data

def addGeocodeData(label,location,geoReferencedLocationsFile):
        emptyDict = {}
        datiGeo_ = pd.read_csv(geoReferencedLocationsFile)
        datiGeo = datiGeo_.reindex(columns=['alias_city','alias_address','type','geocode','geometry']).copy()
        #TODO: sollecare un'eccezzione se foundDatiGeo è null non
        foundDatiGeo = datiGeo[(datiGeo['alias_city']==location[0]) & (datiGeo['alias_address']==location[1])]

        #if len(foundDatiGeo) == 0: raise KeyError
        if len( foundDatiGeo ) == 0: return emptyDict #Return nan
        foundDatiGeo.reset_index(inplace=True)
        geocodeLabelList = []
        for i in foundDatiGeo.index:
            geometry = foundDatiGeo.iloc[i]['geometry']
            geoname = foundDatiGeo.iloc[i]['geocode']
            geocodeLabel = label.copy()
            geocodeLabel['location'] = location
            geocodeLabel['geometry'] = geometry
            geocodeLabel['geoname'] = geoname
            geocodeLabelList.append(geocodeLabel)
        return geocodeLabelList

def to_geojson(geoLabel):
    import pandas as pd
    location = geoLabel['location']
    separator = ', '
    location = separator.join( location )
    prop = {"geoname":geoLabel['geoname'],"gestore":geoLabel['gestore'],"web":geoLabel['web'],"report":geoLabel['report'],"timestamp":geoLabel['timestamp'],"cod_gestore":geoLabel['id_gestore']}
    #prop = {"geoname": geoLabel['geoname'], "gestore": geoLabel['gestore'], "web": geoLabel['web'],
    #        "report": geoLabel['report'], "data": geoLabel['data'], "reference": location,
    #        "timestamp": geoLabel['timestamp'], "cod_gestore": geoLabel['id_gestore']}
    parms_ = geoLabel['parameters']
    #Sostituisce il punto decimale con la virgola
    parms = {str(k):str(v).replace(',','.') for k,v in parms_.items()}
    #parms = {str(k):str(v)+' '+par.getUM(str(k)) for k,v in parms_.items()}
    prop.update(parms)
    s = geoLabel['geometry']

    if pd.isna(s):
        raise Exception('Geometry not found for %s', location )
    else:
        geo = geojson.loads( s.replace( "'", '"' ) )
        feature = geojson.Feature( geometry=geo, properties=prop )
        return feature

def to_GeoJsonFeature(label,locations,geoReferencedLocationsFile):
    import numpy as np
    #Crea il dizionario delle location per accesso ad dati georeferenziati. datiGeo è il dizionario
    datiGeo_ = pd.read_csv( geoReferencedLocationsFile )
    datiGeo = datiGeo_.reindex( columns=['alias_city', 'alias_address', 'geocode', 'geometry'] )
    datiGeo = datiGeo.set_index( ['alias_city', 'alias_address'] )
    if not datiGeo.index.is_unique: raise DictionaryNotUnique(
        'Dictionary geoReferencedLocations not unique. Let checks it!' )
    datiGeo = datiGeo.to_dict( orient='index' )

    for location in locations:
        geometry = geojson.loads(datiGeo[location]['geometry'])
        geocode = geojson.loads(datiGeo[location]['geocode'])
    return np.nan

def createJSONLabels(gestore,dataReportCollectionFile,geoReferencedLocationsListFile):
    import acqua.label as al
    import acqua.labelCollection as coll
    import logging, pandas as pd
    import numpy as np
    dataReportCollection = pd.read_csv( dataReportCollectionFile )
    ll = []
    for i, reportFound in dataReportCollection.iterrows():
        alias = (reportFound['alias_city'], reportFound['alias_address'])
        logging.info( '>>> %s[%s]...', alias, i )
        label = reportFound.dropna().to_dict()
        #data_report = reportFound['data_report']
        lb = al.create_label( np.nan, gestore, np.nan, label )
        glb = al.addGeocodeData( lb, alias, geoReferencedLocationsListFile )
        ll.extend( glb )
        logging.info( 'Done.' )
    fc = coll.to_geojson( ll )
    coll.to_file( fc, gestore + '.geojson' )
    return fc