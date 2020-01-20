import tabula
import os
filename = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/AceGasAmga/2019_11_novembre_TS.1577977068.pdf'
table = tabula.read_pdf( filename, stream=True, pages="all")

a = table['parametro']
print(a)

table_ = table.reindex(columns=['Prova','Prova U.M.','Risultato'])
table2 = table_.dropna(axis=1,how='all')
a = table2['Prova U.M.']
a.to_csv('index.txt')



