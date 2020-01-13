##
import logging
import pandas as pd
##
def get_table(url_report):
    import tabula
    row_table = tabula.read_pdf(url_report, stream=True,pages="all")
    row_table2 = row_table.T.reset_index().T
    return row_table2

url_report1 = 'FriuliVeneziaGiulia/HydroGEA/Definitions/Andreis - caratteristiche acqua HYDROGEA.pdf'
url_report2 = 'FriuliVeneziaGiulia/HydroGEA/Definitions/Arba - caratteristiche acqua HYDROGEA.pdf'
url_report3 = 'FriuliVeneziaGiulia/HydroGEA/Definitions/Aviano - caratteristiche acqua HYDROGEA.pdf'
url_report4 = 'FriuliVeneziaGiulia/HydroGEA/Definitions/Pordenone - caratteristiche acqua HYDROGEA.pdf'
url_report5 = 'FriuliVeneziaGiulia/HydroGEA/Definitions/Barcis - caratteristiche acqua HYDROGEA.pdf'
#import camelot
#tables = camelot.read_pdf(url_report)
#print(tables[0].parsing_report)
#row_table = tables[0].df
row_table1 = get_table(url_report1)
#row_table2 = get_table(url_report2)
#row_table3 = get_table(url_report3)
#row_table4 = get_table(url_report4)
#row_table5 = get_table(url_report5)



##
parms = ['ph', 'Residuo fisso a 180°','Resid. fisso 180°', 'Durezza', 'Conducibilità', 'Calcio', 'Magnesio', 'Ammonio', 'Cloruri',
         'Solfati', 'Potassio', 'Sodio', 'Arsenico', 'Bicarbonato', 'Cloro residuo', 'Fluoruri', 'Nitrati', 'Nitriti',
         'Manganese']
##
def estractLabelFromRawTable(comune,rawTable):
    import numpy as np
    table = rawTable.reset_index()
    boolMatrix = table.apply(lambda x: x.str.contains(comune, na=False))
    alias_coordinates = np.where(boolMatrix)
    alias_address = table.iloc[alias_coordinates]
    rowFound = alias_coordinates[0]
    columnFound = alias_coordinates[1]
    if len(rowFound)==0 or len(columnFound)==0 : raise Exception(comune,"not found.")
    table.set_index(0,inplace=True)
    label = table.loc[parms,columnFound-1]
    label_cleaned = label.dropna()
    ll = {}
    ll['alias_address'] = comune
    ll['label'] = label_cleaned.to_dict(orient='index')
    return ll

##
alias_address = 'Bosplans'
#alias_address = 'Montisel'
#alias_address = 'Alcheda'

#alias_address = 'Canaletto'
#alias_address =  'Via San Daniele'

#alias_address =  '“Colle di Arba”'

#alias_address =  'Fornel'
#alias_address =  'Clap Pisul'
#alias_address =  'Pedemonte'
#alias_address =  'Giais S. Martino'
#alias_address =  'Piancavallo'
#alias_address =  'V. Cima Manera'

#alias_address =  'Losie  - Cuol Alto'
#alias_address =  'Cuol Basso'
#alias_address =  'Guar'
#alias_address =  'Pazolar'
#alias_address =  'Molassa'

a = estractLabelFromRawTable(alias_address,row_table1)
print(a)
