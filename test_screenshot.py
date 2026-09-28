import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8001/login')
time.sleep(5)

driver.save_screenshot("login_test.png")

logs = driver.get_log('browser')
print("BROWSER LOGS:")
for entry in logs:
    print(entry)

driver.quit()
