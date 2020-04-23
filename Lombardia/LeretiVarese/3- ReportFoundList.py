##
from bs4 import BeautifulSoup
import requests
import pandas as pd,logging
import acqua.aqueduct as aq
import pdfquery,io
gestore = "LeretiVarese"
aq.setEnv('Lombardia//'+gestore)
urlSite = 'http://www.leretispa.it/l-acqua-che-bevi'
sitePrefix = 'http://www.leretispa.it'
page = requests.get(urlSite)
soup = BeautifulSoup(page.text, 'html.parser')
#
def getZona(pdf,page):
    label = 'Zona:'
    def clean_text(text):  return text.replace(label,'').strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner, left_corner+400, bottom_corner+20)
    text = pdf.pq(s).text()
    return clean_text(text)

def getLocations(pdf,page):
    def clean_text(text):  return [t.strip() for t in text if t!=""]
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (page, 150, 80, 440, 275)
    text = pdf.pq(s).text()
    cites = text.split( "," )
    return clean_text(cites)

def getDataReport(pdf,page):
    label = "Dati aggiornati al"
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" % (page, label)
    text = pdf.pq( q ).text()
    data_report = text.split( label )[1]
    return data_report
#
anchors = soup.select("p a")
urlReports = [a.parent.select("a")[0]['href'].split(".pdf")[0]+".pdf" for a in anchors]
alias_city = []
alias_address = []
page = []
urlReport = []
data_report = []
#
#urlReports = urlReports[29:30]
for i,urlRep in enumerate(urlReports):
    try:
        logging.info( "Reading %s (%s/%s) ...", urlRep, i + 1, len( urlReports ) )
        url = sitePrefix + urlRep if urlRep[0]=='/' else urlRep
        file = io.BytesIO( requests.get( url ).content )
        pdf = pdfquery.PDFQuery( file )
        pdf.load()
        pages = len( pdf._pages )
        ##
        for p in range(0, pages):
            #p=0
            zona = getZona( pdf, p)
            indirizzi = getLocations( pdf, p)
            data = getDataReport( pdf, p)
            address = ['Comune'] if len(indirizzi)==0 else indirizzi
            alias_address.extend( address )
            alias_city.extend( [zona for i in address]  )
            page.extend( [p for i in address] )
            urlReport.extend( [url for i in address] )
            data_report.extend( [data.strip() for i in address] )
    except:
        logging.critical("Skip %s",urlRep)
##
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'page':page,'urlReport':urlReport,'data_report':data_report})
reportFoundList.to_csv('Metadata/DataReportCollection.csv',index=False)