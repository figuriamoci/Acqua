import pandas as pd
import os
import logging
os.chdir('/Users/andrea/PycharmProjects/Acqua')
logging.basicConfig(level=logging.INFO)
logging.info("Loading Gestori acqua")
fileGestori = 'resource/ANAGRAFICA_GESTORI.csv'
df_ = pd.read_csv(fileGestori,encoding='utf-8')
df = df_.reindex(columns=['descrizione_gestore','url_qualita_acqua','sito_internet','id_gestore'])
df.set_index('id_gestore',inplace=True)
gestori = df.to_dict(orient='index')

def name(id_gestore):
    return gestori[id_gestore]

def setEnv(path):
    logging.basicConfig( level=logging.INFO )
    path = path
    #os.chdir( "D://Python//Acqua" )
    os.chdir( "/Users/andrea/PycharmProjects/Acqua/")
    os.chdir(path)
    return path


def createChoroplethFormDB(geoReferencedLocationsFile,reteAcquedottiFile,output_file):
    import pandas as pd, folium, os, logging, geojson
    from folium.plugins import MarkerCluster  # for clustering the markers

    points = pd.read_csv( geoReferencedLocationsFile )

    pointNotNull_ = points[-points['geometry'].isnull()]
    points = pointNotNull_['geometry']
    firstPoint = points.iloc[0]
    firstPointGeoJSON = geojson.loads( firstPoint.replace( "'", '"' ) )


    map = folium.Map( location=[firstPointGeoJSON['coordinates'][1], firstPointGeoJSON['coordinates'][0]],control_scale=True )

    from shapely.geometry import Point, Polygon
    with open( reteAcquedottiFile ) as f: fc = geojson.load( f )
    listFeature = fc['features']
    f = pd.DataFrame()
    for i,feature in enumerate(listFeature):
        a = feature['geometry']['coordinates'][0]
        if len(a)>=1: a = a[0]
        poligonGeoJson = Polygon(a)
        n = 0
        for j,poi in enumerate(points):
             b = geojson.loads( poi.replace( "'", '"' ) )
             c = b['coordinates']
             pointJson = Point(c)
             if pointJson.within(poligonGeoJson): n += 1

        item = {'name':feature['properties']['name'],'points' : int(n)}
        f = f.append(item,ignore_index=True)
    ##
    a = dict(fc)
    map.choropleth( geo_data = fc,name='Aree di uniformità parametrica',data=f,columns=['name','points'],fill_color='YlGn', fill_opacity=0.5, line_opacity=0.9,legend_name="Nummero parametri per area di uniformità",key_on='feature.properties.name')

    pointLayer = folium.FeatureGroup( name='Punti parametrici', show=True )
    map.add_child( pointLayer )
    marker_cluster = MarkerCluster().add_to( pointLayer )  # create marker clusters

    map.add_child( pointLayer )
    # add a marker for every record in the filtered data, use a clustered view
    for i, location in pointNotNull_.iterrows():
        # logging.info('Create Marker for (%s) %s',i,location)
        point = geojson.loads( location['geometry'].replace( "'", '"' ) )
        latitude = point['coordinates'][1]
        longitude = point['coordinates'][0]
        geocode = location['geocode']
        alias = location['alias_city'] + '/' + location['alias_address']
        folium.Marker( [latitude, longitude],popup=geocode, icon=folium.Icon( color='blue', icon='info-sign' ),tooltip=alias ).add_to( marker_cluster )

    folium.LayerControl().add_to( map )
    logging.info( 'Saving new maps...' )
    map.save( output_file )



