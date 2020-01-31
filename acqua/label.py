import acqua.parametri as sp
import acqua.parametri as par
import pandas as pd
import acqua.aqueduct as aq
import time, geojson,numpy as np,logging,math

def create_label (id_gestore,data_report,parms):
    data = {}
    data['gestore'] = id_gestore
    man = aq.name(id_gestore)
    data['gestore'] = man['descrizione_gestore']
    data['web'] = man['sito_internet']
    data['report'] = man['url_qualita_acqua']
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime( "%d/%m/%Y, %H:%M", named_tuple )
    data['timestamp'] = time_string
    data['data'] = data_report
    parameters = {sp.getSTDParm(k): str(v).replace(' ','') for k, v in parms.items()}
    data['parameters'] = parameters
    return data

def addGeocodeData(label,location,geoReferencedLocationsFile):
        emptyDict = {}
        datiGeo_ = pd.read_csv(geoReferencedLocationsFile)
        datiGeo = datiGeo_.reindex(columns=['alias_city','alias_address','type','geocode','geometry']).copy()
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

def to_geojson(geoLabel,rgb):
    location = geoLabel['location']
    separator = ', '
    location = separator.join( location )
    prop = {"geoname":geoLabel['geoname'],"gestore":geoLabel['gestore'],"web":geoLabel['web'],"report":geoLabel['report'],"data":geoLabel['data'],"reference":location,"timestamp":geoLabel['timestamp']}
    parms_ = geoLabel['parameters']
    parms = {str(k):str(v)+' '+par.getUM(str(k)) for k,v in parms_.items()}
    prop.update(parms)
    s = geoLabel['geometry']

    if pd.isna(s):
        logging.critical( 'Geometry not found for %s', location )
        return ''
    else:
        geo = geojson.loads( s.replace( "'", '"' ) )
        type = geo['type']
        if type == 'Polygon':
            extra = {"fill": "#" + rgb}
        elif type == 'Point':
            extra = { "marker-color": "#" + rgb, "marker-size": "small"}
        else:
            extra = {}
            prop.update( extra )

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





