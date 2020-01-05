import PyPDF2 as py
import os
os.path.abspath('2401.pdf')
filename = '/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/CAFC/2401.pdf'
f = open(filename,'rb')
mypdf = py.PdfFileReader(f)


print(f,mypdf,mypdf.getNumPages())
print(mypdf.getPage(0).extractText())


Concentrazione di ioni idrogeno
Conduttività a 200 C
Torbidità
Calcio
Magnesio
Durezza
Fluoruro
Nitrato
Cloruro
Solfati
Ferro
Cromo
Piombo
Cadmio
Sodio
Potassio
Manganese
Nitrito
Ammonio
Residuo fisso a 180C
Arsenico
Selenio
Antimonio
Mercurio
Alluminio
Rame
Niche'
Vanadio
Zinco
Boro 
