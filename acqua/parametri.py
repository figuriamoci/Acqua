# Descrizione dei parametri
DescrizioneParametro = {'RESIDUO_FISSO': 'Residuo fisso', 'DUREZZA': 'Durezza', 'PH': 'pH', 'CALCIO': 'Calcio',
                        'SODIO': 'Sodio', 'MAGNESIO': 'Magnesio', 'POTASSIO': 'Potassio', 'SOLFATO': 'Solfato',
                        'NITRATO': 'Nitrato', 'NITRITO': 'Nitrito', 'CLORURO': 'Cloruro',
                        'CONDUCIBILITA': 'Conducibilita ', 'FLUORURI': 'Fluoruri', 'AMMONIACA': 'Ammoniaca',
                        'MANGANESE': 'Manganese', 'ARSENICO': 'Arsenico', 'BICARBONATO': 'bicarbonato',
                        'CLORO_RESIDUO': 'cloro residuo libero'}
# UnitÃ  di misura parametri
UMParametro = {'RESIDUO_FISSO': 'mg/l', 'DUREZZA': '°F', 'PH': "unità pH", 'CALCIO': 'mg/l', 'SODIO': 'mg/l',
               'MAGNESIO': 'mg/l Mg', 'POTASSIO': 'mg/l K', 'SOLFATO': 'mg/l SO4', 'NITRATO': 'mg/l',
               'NITRITO': 'mg/l', 'CLORURO': 'mg/l Cl', 'CONDUCIBILITA': 'µS/cm', 'FLUORURI': 'mg/L',
               'AMMONIACA': 'mg/L', 'MANGANESE': 'µg/L', 'ARSENICO': 'µg/L', 'BICARBONATO': 'mg/L',
               'CLORO_RESIDUO': 'mg/l'}
# Limiti di legge (D.lgs 31/01)
VLParametro = {'RESIDUO_FISSO': '1500', 'DUREZZA': '15-50 valori consigliati', 'PH': '6,5-9,5',
               'CALCIO': 'non previsto', 'SODIO': '200', 'MAGNESIO': 'non previsto', 'POTASSIO': 'non previsto',
               'SOLFATO': '250', 'NITRATO': '50', 'NITRITO': '0,5', 'CLORURO': '250', 'CONDUCIBILITA': '2500',
               'FLUORURI': '1,5', 'AMMONIACA': '0,5', 'MANGANESE': '50', 'ARSENICO': '10',
               'BICARBONATO': 'non previsto', 'CLORO_RESIDUO': 'non previsto'}

# TODO: Implement Nested Dictionaries

SinonimiParametro = {}

import csv
import os
print(os.path.abspath("Definitions/SynParametri.csv"))
with open('Definitions/SynParametri.csv', newline='', mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        for col in ('syn0', 'syn1', 'syn2', 'syn3', 'syn4', 'syn5', 'syn6', 'syn7', 'syn8', 'syn9'):
            if row[col] is not None:
                SinonimiParametro[row[col]] = row['parametro'].lower()

def getSTDParm(parm):
    return SinonimiParametro[parm.lower()]

def getDescrizione(key):
    v = DescrizioneParametro[key.upper()]
    return v

def getUM(key):
    v = UMParametro[key.upper()]
    return v

def getVL(key):
    v = VLParametro[key.upper()]
    return v