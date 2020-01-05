#Descrizione dei parametri
DescrizioneParametro = {'RESIDUO_FISSO':'Residuo fisso','DUREZZA':'Durezza','PH':'pH','CALCIO':'Calcio','SODIO':'Sodio','MAGNESIO':'Magnesio','POTASSIO':'Potassio','SOLFATO':'Solfato','NITRATO':'Nitrato','NITRITO':'Nitrito','CLORURO':'Cloruro','CONDUCIBILITA':'Conducibilità','FLUORURI':'Fluoruri','AMMONIACA':'Ammoniaca','MANGANESE':'Manganese','ARSENICO':'Arsenico','BICARBONATO':'bicarbonato','CLORO_RESIDUO':'cloro residuo libero'}
#Unità di misura parametri
UMParametro = {'RESIDUO_FISSO':'mg/l','DUREZZA':'°F','PH':'unità pH','CALCIO':'mg/l Ca','SODIO':'mg/l Na','MAGNESIO':'mg/l Mg','POTASSIO':'mg/l K','SOLFATI':'mg/l SO4','NITRATI':'mg/l NO3','NITRITI':'mg/l NO2','CLORURI':'mg/l Cl','CONDUCIBILITA':'µS/cm 20°C','FLUORURI':'mg/L F','AMMONIO':'mg/L NH4','MANGANESE':'µg/L Mn','ARSENICO':'µg/L As','BICARBONATO':'mg/L','CLORO_RESIDUO':'mg/l'}
#Limiti di legge (D.lgs 31/01)
VLParametro = {'RESIDUO_FISSO':'1500','DUREZZA':'15-50 valori consigliati','PH':'6,5-9,5','CALCIO':'non previsto','SODIO':'200','MAGNESIO':'non previsto','POTASSIO':'non previsto','SOLFATO':'250','NITRATO':'50','NITRITO':'0,5','CLORURO':'250','CONDUCIBILITA':'2500','FLUORURI':'1,5','AMMONIACA':'0,5','MANGANESE':'50','ARSENICO':'10','BICARBONATO':'non previsto','CLORO_RESIDUO':'non previsto'}


print(DescrizioneParametro['RESIDUO_FISSO'])
print(UMParametro['RESIDUO_FISSO'])
print(VLParametro['RESIDUO_FISSO'])


#TODO: Implement Nested Dictionaries

SinonimiParametro = {}

import csv
with open('SynParametri.csv', newline='', mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        for col in ('syn0','syn1','syn2','syn3','syn4','syn5','syn6','syn7','syn8','syn9'):
            if row[col] is not None:
                SinonimiParametro[row[col]] = row['parametro']
print(SinonimiParametro)

def getSTDParm(parm):
    return SinonimiParametro[parm.lower()]

