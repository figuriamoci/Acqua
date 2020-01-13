import acqua.parametri as sp
import acqua.parametri as par
import pandas as pd

def create_label (id_gestore,data_report,parms):
    data = {}
    data['gestore'] = id_gestore
    data['data_report'] = data_report
    
    parameters = {}
    parameters = {sp.getSTDParm(k): str(v).replace(' ','') for k, v in parms.items()}
    data['parameters'] = parameters
    
    return data

def addGeocodeData(label,location,geoReferencedLocationsFile):
        emptyDict = {}
        datiGeo = pd.read_csv(geoReferencedLocationsFile)
        datiGeo = datiGeo.set_index(['alias_city','alias_address'])
        datiGeo = datiGeo.to_dict(orient='index')
        #Recupera dati geo di tipo Poin
        try:
            geometry = datiGeo[location]['geometry']
            geocode = datiGeo[location]['geocode']
            geocodeLabel = label.copy()
            geocodeLabel['location'] = location
            geocodeLabel['geometry'] = geometry
            geocodeLabel['geocode'] = geocode
            if pd.isnull(geocode):
                return emptyDict
            else:
                return geocodeLabel
        except KeyError:
            return emptyDict
            

def to_geojson(geoLabel):
    try:
        geometry = geoLabel['geometry']
        geojson = '{"type":"Feature","geometry": '+geometry.replace("'",'"')+','
        location = geoLabel['location']
        separator = ', '
        location_ = separator.join(location)
        properties = '"properties": { "name": "'+location_+'"'
        parms = geoLabel['parameters']
        for k in parms: properties = properties + ', "'+str(k)+'": "'+str(parms[k])+' '+par.getUM(str(k))+'"'
        return geojson+properties+'}}'
    except KeyError:
        return ''
