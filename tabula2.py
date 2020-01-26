import tabula
import os
filename = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque/Definitions/Primosemestre2019.pdf'
table = tabula.read_pdf( filename, stream=True, pages="all")

a = table['parametro']
print(a)

table_ = table.reindex(columns=['Prova','Prova U.M.','Risultato'])
table2 = table_.dropna(axis=1,how='all')
a = table2['Prova U.M.']
a.to_csv('index.txt')



