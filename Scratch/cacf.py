from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("D:\EmporioADV\chromedriver", chrome_options=options)
driver.get("https://www.cafcspa.com/solud/it-_qualita_acqua.cfm")

#import requests
#url = 'https://www.cafcspa.com/solud/it-_qualita_acqua.cfm'
#page = requests.get(url)
#page.status_code
#page.text

#https://selenium-python.readthedocs.io/navigating.html


select_comuni = driver.find_element_by_id("comuni")
list_comuni = select_comuni.find_elements_by_tag_name("option")

#for comune in list_comuni: print(comune.get_attribute("text"))

for comune in list_comuni:
    #print(comune.get_attribute("text"))
    comune.click()
    #lista_localita = comune.find_elements_by_tag_name('indirizzi')
    


    
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(driver.page_source,'html.parser')#
#l = soup.find_next('select')




#more_buttons = driver.find_element_by_id("comuni")
#more_buttons[0].is_displayed()


#for x in range(len(more_buttons)):
#  if more_buttons[x].is_displayed():
#      driver.execute_script("arguments[0].click();", more_buttons[x])
#      time.sleep(1)
#page_source = driver.page_source
