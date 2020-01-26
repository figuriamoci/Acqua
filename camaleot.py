##
import camelot
tables = camelot.read_pdf( '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/IRISAcque/Definitions/Primosemestre2019.pdf')
tables
##
tables.export('foo.csv', f='csv', compress=True) # json, excel, html
a = tables[0]
##
print(tables[0].parsing_report)