import acqua.parametri as sp
import acqua.parametri as par
import pandas as pd
import acqua.aqueduct as aq
import time
import geojson as geo

def create_label (id_gestore,data,parms):
    data = {}
    data['gestore'] = id_gestore
    man = aq.name(id_gestore)
    data['gestore'] = man['descrizione_gestore']
    data['web'] = man['sito_internet']
    data['report'] = man['url_qualita_acqua']
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime( "%d/%m/%Y, %H:%M", named_tuple )
    data['timestamp'] = time_string
    data['data'] = data
    
    parameters = {}
    parameters = {sp.getSTDParm(k): str(v).replace(' ','') for k, v in parms.items()}
    data['parameters'] = parameters
    
    return data

def addGeocodeData(label,location,geoReferencedLocationsFile):
        emptyDict = {}
        datiGeo_ = pd.read_csv(geoReferencedLocationsFile)
        datiGeo = datiGeo_.reindex(columns=['alias_city','alias_address','geocode','geometry']).copy()

        datiGeo2 = (datiGeo['alias_city']==location[0]) & (datiGeo['alias_address']==location[1])
        datiGeo3 = datiGeo[datiGeo2]

        if len(datiGeo3) == 0: raise KeyError
        datiGeo3.reset_index(inplace=True)
        loc = datiGeo3.index

        geocodeLabelList = []
        for i in datiGeo3.index:
            geometry = datiGeo3.iloc[i]['geometry']
            geocode = datiGeo3.iloc[i]['geocode']
            geocodeLabel = label.copy()
            geocodeLabel['location'] = location
            geocodeLabel['geometry'] = geometry
            geocodeLabel['geoname'] = geocode
            geocodeLabelList.append(geocodeLabel)

        return geocodeLabelList

def to_geojson(geoLabel):
    try:
        geometry = geoLabel['geometry']
        geojson = '{"type":"Feature","geometry": '+geometry.replace("'",'"')+','
        location = geoLabel['location']
        separator = ', '
        location_ = separator.join(location)
        properties = '"properties": { "name": "'+location_+'",'
        properties = properties+'"name": "' + location_ + '",'
        properties = properties + '"geoname": "' + geoLabel['geoname'] + '",'
        properties = properties + '"gestore": "' + geoLabel['gestore'] + '",'
        properties = properties + '"web": "' + geoLabel['web'] + '",'
        properties = properties + '"report": "' + geoLabel['report'] + '",'
        properties = properties + '"timestamp": "' + geoLabel['timestamp'] + '"'
        parms = geoLabel['parameters']
        for k in parms: properties = properties + ', "'+str(k)+'": "'+str(parms[k])+' '+par.getUM(str(k))+'"'
        return geojson+properties+'}}'
    except KeyError:
        return ''

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





