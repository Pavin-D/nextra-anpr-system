import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8001/login')
time.sleep(2)

print("BROWSER LOGS:")
for entry in driver.get_log('browser'):
    print(entry)

driver.quit()
