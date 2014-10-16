from selenium import webdriver
from bs4 import BeautifulSoup
import time
import unicodedata

url = 'http://www.smogon.com/dex/xy/pokemon/abomasnow'
driver = webdriver.Firefox()
driver.get(url)
time.sleep(2)
more2load = True
while more2load:
    old_len = len(driver.page_source)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.1)
    new_len = len(driver.page_source)
    if old_len == new_len:
        more2load = False        
soup = BeautifulSoup(driver.page_source)
driver.close()

legal_moves = []
move_table = soup.find("table", {"class" : "MoveTable"})
rows = move_table.findAll('tr')
for r in rows:
    raw_name = r.findAll('td')[0].text
    move_name = unicodedata.normalize('NFKD', raw_name).encode('ascii', 'ignore')
    legal_moves += [move_name]