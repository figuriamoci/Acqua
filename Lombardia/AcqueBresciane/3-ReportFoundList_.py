##
from bs4 import BeautifulSoup
import pandas as pd,logging,requests,io
import pdfquery
import acqua.aqueduct as aq
gestore = "AcqueBresciane"
aq.setEnv('Lombardia//'+gestore)
url = 'https://www.acquebresciane.it/public/acquebresciane-portal/it/home/qualita-acqua'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
site = 'https://www.acquebresciane.it'
#
anchors = soup.findAll("a", {"class": "readme-links__abstract appr-element-links"})
reportUrls = [site+url['href'] for url in anchors if url['href'] != ""]
#
alias_city = []
alias_address = []
urlReport = []
data_report = []
page = []
def getText(pdf,label,page):
    def clean_text(text):  return text.replace(label,'').strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner, left_corner+400, bottom_corner+20)
    text = pdf.pq(s).text()
    return clean_text(text)
##
#reportUrls = reportUrls[77:79]
for i,url in enumerate(reportUrls):
    logging.info("Reading %s (%s/%s) ...",url,i+1,len(reportUrls))
    file = io.BytesIO(requests.get(url).content)
    pdf = pdfquery.PDFQuery(file)
    pdf.load()
    pages = len(pdf._pages)
    ##
    for p in range(pages-1):
        comune = getText(pdf,'COMUNE:',p )
        alias_city.append(comune)
        indirizzo = getText( pdf, 'AREA DI ANALISI:', p )
        alias_address.append( indirizzo )
        urlReport.append(url)
        page.append(p)
        periodo = getText( pdf, 'PERIODO DI ANALISI:', p )
        data_report.append(periodo)
    #
    logging.info("Hacked %s locations for %s !",pages,comune)

##
reportFoundList = pd.DataFrame({'alias_city':alias_city,'alias_address':alias_address,'urlReport':urlReport,'page':page,'data_report':data_report})
reportFoundList.to_csv('Metadata/DataReportCollection.csv',index=False)
