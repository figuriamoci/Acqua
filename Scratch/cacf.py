from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
driver.get("https://www.cafcspa.com/solud/it-_qualita_acqua.cfm")
#driver.get('https://www.seleniumeasy.com/test/basic-select-dropdown-demo.html')

#import requests
#url = 'https://www.cafcspa.com/solud/it-_qualita_acqua.cfm'
#page = requests.get(url)
#page.status_code
#page.text

#https://selenium-python.readthedocs.io/navigating.html

from selenium.webdriver.support.ui import Select
import pandas as pd

#import requests
#page_source = requests.get('https://www.cafcspa.com/solud/it-_qualita_acqua.cfm')


from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source,'html.parser')#
#soup = BeautifulSoup(page_source.text,'html.parser')#
print(soup.prettify())
soup.find('select')

select_comuni = Select(driver.find_element_by_id("comuni"))
#list_comuni = select_comuni.find_elements_by_tag_name("option")
select_comuni.select_by_visible_text('AIELLO DEL FRIULI')
soup = BeautifulSoup(driver.page_source,'html.parser')#

print(soup.prettify())
tbl = soup.findAll('select')[1]
tbl
tbl[1].get_text()
data_frame = pd.read_html(str(tbl),decimal=',',thousands=',',index_col=0,header=0)[0]


select[1].get_text()



#for comune in list_comuni: print(comune.get_attribute("text"))
#select_indirizzi = driver.find_element_by_id("indirizzi")

for indirizzo in select_indirizzi: print(indirizzo.get_attribute("text"))
    #comune.click()
    #select_comuni.select_by_visible_text(comune)
    #lista_localita = comune.find_elements_by_tag_name('indirizzi')
    
#select = Select(driver.find_element_by_id('fruits01'))

# select by visible text
#select.select_by_visible_text('Banana')

# select by value 
#select.select_by_value('1')

    
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
