class GeoPointLabel:
    """Class for creating and managing geo water labels"""
    def __init__(self,label):
        #Imposta eticheta
        import pandas as pd
        self.label = label
        #Recupera i dati Geo di definizione
        datiGeo = pd.read_csv('Definitions/GeoReferencedLocationsList.csv')
        datiGeo = datiGeo.set_index('alias')
        datiGeo = datiGeo.to_dict(orient='index')
        #Recupera dati geo di tipo Point
        self.name = datiGeo[label.getAlias()]['name']
        self.geocode = datiGeo[label.getAlias()]['geocode']
        self.latitude = datiGeo[label.getAlias()]['latitude']
        self.longitude = datiGeo[label.getAlias()]['longitude']
        
    def getLabel(self):
        return self.label
      
    def to_geojson(self):
        import resource.Parametri as par
        geojson = '{"type":"Feature","geometry": {"type": "Point","coordinates": ['+str(self.longitude)+','+str(self.latitude)+']},'
        properties = '"properties": { "name": "'+self.name+'"'
        parms = self.getLabel().getParameters()
        for k in parms: properties = properties + ', "'+str(k)+'": "'+str(parms[k])+' '+par.getUM(str(k))+'"'
        return geojson+properties+'}}'
 
    def __str__(self):
        """Template printing"""
        return "geocode: "+self.geocode+", latitude: "+str(self.latitude)+", longitude: "+str(self.longitude)+", label: "+str(self.label)
