pdf_path = "https://www.cafcspa.com/solud/analisi/D702.pdf"
pdf_path = 'https://www.cafcspa.com/solud/analisi/2401.pdf'

import tabula
import pandas as pd
pd = tabula.read_pdf(pdf_path, stream=True, pages="all")
pd

#import camelot
#tables = camelot.read_pdf(pdf_path)
#print(tables)
