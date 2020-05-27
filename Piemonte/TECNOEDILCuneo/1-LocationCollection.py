##
from bs4 import BeautifulSoup
import io,pdfquery,requests
import requests,logging
import acqua.aqueduct as aq
import pandas as pd
logging.basicConfig(level=logging.INFO)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "TECNOEDILCuneo"
aq.setEnv('Piemonte//'+gestore)
url = 'http://www.egea.it/idrico/ciclo-idrico-integrato/analisi-tecnoedil/'
def cityRectCoordinates():
    #leftUpperCorner
    q = "LTPage[page_index='0'] LTTextLineHorizontal:contains('%s')" % 'Comuni serviti dalla fonte'
    textLine = pdf.pq( q )
    leftCorner = float( textLine.attr( 'x1' ) )
    upperCorner = float( textLine.attr( 'y1' ) )+3 #Un po di tolleranza che non guasta
    #bottomRightCorner
    q = "LTPage[page_index='0'] LTTextLineHorizontal:contains('%s')" % 'Ente gestore'
    textLine = pdf.pq( q )
    rightCorner = 400
    bottomCorner = float( textLine.attr( 'y1' ) )
    return {'x0':leftCorner,'y0':upperCorner,'x1':rightCorner,'y1':bottomCorner}
#
def city_elements():
    rect = cityRectCoordinates()
    return float( this.get( 'y0', 0 ) ) >= rect['y1'] and float( this.get( 'y1', 0 ) ) <= rect['y0'] and float(
        this.get( 'x0', 0 ) ) >= rect['x0']
#
webPage = requests.get( url )
soup = BeautifulSoup( webPage.text, 'html.parser' )
div = soup.find(id="coldx")
address = div.find_all('address')
urlReport = [a.find('a')['href'] for i,a in enumerate(address) if i>1 and a.text.strip() != '']
alias_city = []
##
for i,report in enumerate(urlReport):
    #i=1
    #report = urlReport[i]
    file = io.BytesIO( requests.get( report ).content )
    pdf = pdfquery.PDFQuery( file )
    pdf.load()
    locations = pdf.pq( 'LTPage[page_index="0"] *' ).filter( city_elements )
    alias_city.extend([l.text.strip() for l in locations])
    logging.info('Found %s address for %s', len(locations),report)
#
locationList = pd.DataFrame({'alias_city':alias_city})
locationList['alias_address'] = "Comune"
locationList['georeferencingString'] = locationList['alias_city'].str.replace('FR','')+", CN, Piemonte"
locationList['type'] = 'POINT'
locationList.to_csv('Metadata/LocationList.csv',index=False)
