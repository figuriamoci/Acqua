from bs4 import BeautifulSoup
import pandas as pd,logging,requests,io
import pdfquery
import acqua.aqueduct as aq
gestore = "LeretiVarese"
aq.setEnv('Lombardia//'+gestore)
url = 'http://www.leretispa.it/l-acqua-che-bevi'
file = 'Maccagno.pdf'
#file = io.BytesIO( requests.get( url ).content )
pdf = pdfquery.PDFQuery( file )
pdf.load()
pages = len( pdf._pages )
page=0
s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (page, 150, 80, 440, 240)
text = pdf.pq( s ).text()
cites = text.split(",")

label = "Dati aggiornati al"
q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" % (page, label)
text = pdf.pq( q ).text()
data_report = text.split(label)[1]

a = range(0, 1)
for i in a: print(i)