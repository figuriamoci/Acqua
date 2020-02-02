import os,logging,pandas as pd
import xlrd
os.chdir( '/Users/andrea/PycharmProjects/Acqua/AltoAdige' )
xls_file = '03__Internet-tabella_2018-2017-2016-.xlsx'

xl = pd.read_excel(xls_file, index_col=0)

xl['Comune / Gemeinde']
xl['Punto di prelievo / Entnahmepunkt']
a=xl['Durezza totale F°']