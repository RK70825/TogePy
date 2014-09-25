from selenium import webdriver
from bs4 import BeautifulSoup
import unicodedata
import time

print 'Loading Webpage, please be patient'
driver = webdriver.Firefox()
driver.get('http://www.smogon.com/dex/xy/pokemon/')
time.sleep(0.5)
more2load = True
while more2load:
    old_len = len(driver.page_source)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)
    new_len = len(driver.page_source)
    if old_len == new_len:
        more2load = False

table = driver.find_element_by_xpath('//table/tbody')

driver.close()

table_html = table.get_attribute('innerHTML')
soup = BeautifulSoup(table_html)
table2 = soup.find_all('td')
