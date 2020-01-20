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

