import pandas as pd
import tabula
file = "filename.pdf"
path = 'enter your directory path here'  + file
df = tabula.read_pdf(path, pages = '1', multiple_tables = True)
print(df)


LocationlistAlias = ["Isola\rMorosini","Gorizia","Farra","Cormons","Dolegna","Monfalcone","Ronchi dei\rLegionari","Grado","San Pier\rd'Isonzo"]

im = 'Isola \nMorosini'
n
im.replace('/n',' ')