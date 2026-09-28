import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8001/login')
time.sleep(3)

print("PAGE SOURCE:")
print(driver.page_source)

driver.quit()
