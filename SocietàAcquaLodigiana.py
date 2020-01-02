import time
from selenium import webdriver
driver = webdriver.Chrome('D:\EmporioADV\chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.acqualodigiana.it/acqua-del-rubinetto/');
time.sleep(8) # Let the user actually see something!
WebElement = driver.find_element_by_css_selector("#post-127")
WebElement = driver.find_element_by_css_selector("#su-spoiler-title")                                         

                                                 
#WebElement iframe = driver.findElement(By.cssSelector("#pots-127>iframe"));
#search_box = driver.find_element_by_name('Abbadia Cerreto')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
