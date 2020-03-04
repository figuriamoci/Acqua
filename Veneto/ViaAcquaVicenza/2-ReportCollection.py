##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd,datetime,os,logging,time,re
import acqua.aqueduct as aq
import acqua.parametri as parm
aq.setEnv('Veneto//ViaAcquaVicenza')
url = 'https://www.viacqua.it/it/clienti/acquedotto/qualita-acqua/'

#admitted = ['Ammoniaca (NH4+)','Attività ioni idrogeno''Bicarbonati','Calcio','Cloro residuo','Cloruri','Conduc. elettrica specifica a 20 °C','Durezza totale in gradi francesi','Ferro totale','Fluoruri','Magnesio','Manganese','Nitrati','Nitriti','Potassio','Sodio','Solfati','Torbidità','PFOS','PFOA + PFOS','Somma altri PFAS','Carica batterica a 22 °C','Enterococchi','Escherichia coli']
parametersAdmitted = parm.getParametersAdmitted('Definitions/SynParametri.csv')

logging.basicConfig(level=logging.INFO)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)
driver.get(url)
##
locationList = pd.read_csv('Definitions/LocationList.csv')
reportFoundList = pd.DataFrame()
for i,location in locationList.iterrows():
    alias_city = location['alias_city']
    alias_address = location['alias_address']
    logging.info('>>> %s/%s (%s/%s)',alias_city,alias_address,i,len(locationList)-1)
    Select(driver.find_element(By.ID,'local_comune')).select_by_visible_text(alias_city)
    time.sleep(1)
    Select(driver.find_element(By.ID,'local_impianto')).select_by_visible_text(alias_address)
    ##
    time.sleep(1)
    try:
        htmlTable = driver.find_element(By.ID,'local_document').find_element_by_tag_name('table')
        rowTable = pd.read_html(htmlTable.get_attribute('outerHTML'),thousands='.',decimal=',')[0]
        ##
        premessa = rowTable.iloc[0,0]
        data_report = re.findall('\d\d/\d\d/\d\d\d\d',premessa)[0]
        ##
        parameters_ = rowTable.iloc[:,[0,1]].rename(columns ={0:'parametro',1:'valore'})
        parameters_ = parameters_.set_index('parametro')['valore']
        parameters = parameters_.reindex(parametersAdmitted).to_dict()
        ##
        report = {'alias_city': alias_city, 'alias_address': alias_address, 'data_report': data_report}
        report.update( parameters )
        reportFoundList = reportFoundList.append(report,ignore_index=True)
    except:
        logging.critical('Skip %s/%s.',alias_city,alias_address)
#
driver.close()
reportFoundList.to_csv('Definitions/ReportFoundList.csv',decimal=',',index=False)
logging.info('Finish: %s',datetime.datetime.now())




