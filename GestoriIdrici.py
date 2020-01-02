import pandas as pd
gestori = pd.read_csv('Resource/ANAGRAFICA_GESTORI.csv', encoding='utf-8')

def gestoreAcqua(id): 
    g = gestori[gestori['id_gestore']==id]
    return g[['descrizione_gestore','sito_internet']]

def descrizioneGestore(id): 
    g = gestori[gestori['id_gestore']==id]
    return g[['descrizione_gestore']]

gestoreAcqua(7396)
