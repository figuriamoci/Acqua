##
from selenium import webdriver
import pandas as pd,os
##
os.chdir('/Users/andrea/PycharmProjects/Acqua/FriuliVeneziaGiulia/HydroGEA')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.get("https://www.hydrogea-pn.it/#/menu/informazioni/acqua")
#print('Http status: ',page.status_code)
listLocations = pd.DataFrame()
i=0
webElementsList = driver.find_elements_by_css_selector("div.mapareatxt")
region = 'Pordenone'

for controlWebElement in webElementsList:
    i=i+1
    try:
        driver.implicitly_wait(10)
        comune = controlWebElement.text
        driver.execute_script("arguments[0].click();", controlWebElement)
        window_after = driver.window_handles[i]
        driver.switch_to.window(window_after)
        urlReport = driver.current_url
        row = {'alias_city':comune,'location':comune,'region':region,'urlReport':urlReport}
        listLocations = listLocations.append(row,ignore_index=True)
        driver.switch_to.window(driver.window_handles[0])
    except:
        print('completato!')
        

listLocations.to_csv('Definitions/LocationList.csv',index=False)


