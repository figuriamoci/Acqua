##
import os,camelot
os.chdir('/Users/andrea/PycharmProjects/Acqua')
tables = camelot.read_pdf('FriuliVeneziaGiulia/CAFC/9717.pdf')
tables
##
tables.export('foo.csv', f='csv', compress=True) # json, excel, html
tables[0]
##
tables[0].parsing_report