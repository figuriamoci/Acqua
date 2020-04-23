##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd,logging,time
import acqua.aqueduct as aq
aq.setEnv('FriuliVeneziaGiulia//HydroGEA')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
driver.implicitly_wait( 10 )
driver.get("https://www.hydrogea-pn.it/#/menu/informazioni/acqua")
time.sleep(3)
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "ajs-close"))).click()

reportFoundList = pd.DataFrame()
webElementsList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mapareatxt")))
##
for i,controlWebElement in enumerate(webElementsList):
    try:
        comune = controlWebElement.get_attribute("innerText")
        driver.execute_script("arguments[0].click();", controlWebElement)
        time.sleep(5)
        window_after = driver.window_handles[i]
        driver.switch_to.window(window_after)
        urlReport = driver.current_url
        row = {'alias_city':comune,'alias_address':'','urlReport':urlReport}
        reportFoundList = reportFoundList.append(row,ignore_index=True)
        driver.switch_to.window(driver.window_handles[0])
        logging.info('Get url report fot %s',comune)
    except:
        logging.critical('Skip %s',comune)
##
driver.close()
reportFoundList.to_csv('Medadata/DataReportCollection.csv',index=False)


