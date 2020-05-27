##
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging,pandas as pd
import acqua.aqueduct as aq
import pdfquery,io,requests,warnings,time
warnings.simplefilter(action='ignore', category=FutureWarning)
logging.getLogger( "pdfminer" ).setLevel( logging.WARNING )
gestore = "PaviaAcque"
aq.setEnv('Lombardia//'+gestore)
url = 'http://www.paviaacque.it/attivita/qualita-dellacqua/'
options = webdriver.ChromeOptions()
options.add_argument( '--ignore-certificate-errors' )
options.add_argument( '--incognito' )
options.add_argument( '--headless' )
driver = webdriver.Chrome( "chromedriver", options=options )
driver.implicitly_wait( 20 )  # seconds
driver.get( url )
#
selectComuneWebElement = WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "city" ) ) )
cityList = selectComuneWebElement.text.split('\n')[1:]
#
def getLocation(pdf,label,page):
    def clean_text(text):  return text.split(label)[1].strip()
    q = "LTPage[page_index='%s'] LTTextLineHorizontal:contains('%s')" %(page,label)
    textLine = pdf.pq(q)
    left_corner = float(textLine.attr('x0'))
    bottom_corner = float(textLine.attr('y0'))
    s = 'LTPage[page_index="%s"] LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' %(page,left_corner, bottom_corner-3, left_corner+300, bottom_corner+10)
    text = pdf.pq(s).text()
    return clean_text(text)
#
locationList = pd.DataFrame()
for i,comune in enumerate(cityList):
    #i=1
    #comune = cityList[i]
    #comune='PAVIA'
    logging.info( 'Processing %s...', comune )
    try:
        Select(WebDriverWait( driver, 10 ).until( EC.visibility_of( driver.find_element_by_name( "city" ) ) )).select_by_visible_text(comune)
        #
        time.sleep(5)
        #rowComuneWebElement = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located( driver.find_elements_by_class_name( "block" ) ) )
        rowComuneWebElement = driver.find_elements_by_class_name('block')
        #
        for j,row in enumerate(rowComuneWebElement):
            #j=0
            #row = rowComuneWebElement[j]
            anchor = row.find_element_by_tag_name('a')
            urlReport = anchor.get_attribute('href')
            logging.info('(%s)...',urlReport)
            file = io.BytesIO( requests.get( urlReport ).content )
            pdf = pdfquery.PDFQuery( file )
            pdf.load()
            try:
                location = getLocation( pdf, 'Descrizione Camp.:',0 )
                alias_address = location
            except:
                alias_address=comune
                logging.critical('Perhaps SCANNER report for %s/%s.',comune, alias_address)
            finally:
                row = {'alias_city': comune, 'alias_address': alias_address}
                locationList = locationList.append( row, ignore_index=True )
                logging.info( 'Collect data for %s/%s (%s/%s)', comune, alias_address, i, len( cityList ) - 1 )
            #
    except:
        logging.critical( 'Report not found for %s/%s!', comune, alias_address )
    #
    driver.back()
#
driver.close()
##
locationList_ = locationList.groupby(['alias_city','alias_address']).first()
locationList_.reset_index(inplace=True)
locationList_['georeferencingString'] = locationList_['alias_address'].str.replace('Routine + THM :','').str.strip()+", PV"
locationList_['type'] = 'POINT'
locationList_.to_csv('Metadata/LocationList.csv',index=False)
