import tabula
import os
os.path.abspath('2401.pdf')
filename = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC/2401.pdf'
f = open(filename,'rb')
mypdf = py.PdfFileReader(f)
print(f,mypdf,mypdf.getNumPages())
print(mypdf.getPage(0).extractText())
