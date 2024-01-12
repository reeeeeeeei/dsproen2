from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

#driverオブジェクト生成
driver_path = '/opt/win32/chromedriver-mac-arm64/chromedriver'

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

#amzonのURL
amazon_url = 'https://www.amazon.co.jp/'

#ページを取得
driver.get(amazon_url)

#5秒間ストップ
time.sleep(5)

driver.quit()