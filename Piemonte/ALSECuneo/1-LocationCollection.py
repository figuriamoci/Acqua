##
from bs4 import BeautifulSoup
import io,pdfquery,requests
import requests,logging
import acqua.aqueduct as aq
import pandas as pd
logging.basicConfig(level=logging.INFO)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "ALSECuneo"
aq.setEnv('Piemonte//'+gestore)
url = 'http://www.altalangaservizi.it/Home/Menu?IDDettaglioPagina=45659'
site = 'http://www.altalangaservizi.it'
#
def cityRectCoordinates():
    #leftUpperCorner
    q = "LTPage[page_index='0'] LTTextLineHorizontal:contains('%s')" % 'Comuni serviti dalla fonte'
    textLine = pdf.pq( q )
    leftCorner = float( textLine.attr( 'x0' ) )
    upperCorner = float( textLine.attr( 'y0' ) ) - 3  # Un po di tolleranza che non guasta
    # bottomRightCorner
    q = "LTPage[page_index='0'] LTTextLineHorizontal:contains('%s')" % 'Parametro'
    textLine = pdf.pq( q )
    bottomCorner = float( textLine.attr( 'y1' ) ) + 20
    rightCorner = 400
    return {'x0':leftCorner,'y0':upperCorner,'x1':rightCorner,'y1':bottomCorner}
#
def city_elements():
    rect = cityRectCoordinates()
    return float( this.get( 'y0') ) <= rect['y0'] and float( this.get( 'y1') ) >= rect['y1']
#
webPage = requests.get( url )
soup = BeautifulSoup( webPage.text, 'html.parser' )
div = soup.find(id="dnn_ctr7730_ContentPane")
report = div.find_all('a',{'class':'TabellaAllegatiImmagine'})
urlReport = [site + a['href'].replace('..','') for i,a in enumerate(report)]
alias_city = []
##
for i,report in enumerate(urlReport):
    #i=4
    #report = urlReport[i]
    file = io.BytesIO( requests.get( report ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    locations = pdf.pq( 'LTPage[page_index="0"] *' ).filter( city_elements )
    alias_city.extend([l.text.strip() for l in locations if l.text is not None and l.text.strip() != ''])
    logging.info('Found %s address for %s (%s)', len(locations),report,i)
##
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city']+", CN, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
