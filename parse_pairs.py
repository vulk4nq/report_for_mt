import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
url = 'https://www.binance.com/ru/futures/trading-rules'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(2)

soup = BeautifulSoup(driver.page_source,'html.parser')

cells = soup.find_all(class_='rc-table-cell-fix-left-last')
pairs = []
for cell in cells:
	pairs.append(cell.text[:cell.text.find(' ')])
print(pairs)
f = open('pairs.txt','w')
for pair in pairs:
	f.write(pair+'\n')