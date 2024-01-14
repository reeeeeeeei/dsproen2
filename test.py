# import
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
import csv


chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


HREFS = []

# URL開く
driver.get("https://www.amazon.co.jp/gp/goldbox?ref_=nav_cs_gb")
# 待機処理
sleep(10)
wait = WebDriverWait(driver=driver, timeout=60)
 #検索窓 
Word = "冷蔵庫"
driver.find_element(By.ID, "twotabsearchtextbox").send_keys(Word)
sleep(1)
driver.find_element(By.ID,"nav-search-submit-button").click()
 #商品URLの取得 
URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")

for URL in URLS:
    URL = URL.get_attribute("href")
    print("[INFO] URL :", URL)
    HREFS.append(URL)
 

# CSVファイルのヘッダー
csv_header = ['Title', 'Original Price', 'Discount Price', 'Discount Rate', 'Image']

# CSVファイルが存在しない場合、新しく作成してヘッダーを書き込む
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_header)

#商品詳細の取得とCSVへの書き込み
for HREF in HREFS:
    driver.get(HREF)
    try:
        # title
        title = driver.find_element(By.ID, "productTitle").text.strip()
        # original_price
        original_price = driver.find_element(By.CSS_SELECTOR, 'div.a-section.a-spacing-small.aok-align-center > span > span > span > span > span.a-offscreen').text.strip()
        # discount_price
        discount_price = driver.find_element(By.CSS_SELECTOR, 'div.aok-align-center > span > span > span.a-price-whole').text.strip()
        # discount_rate
        discount_rate = driver.find_element(By.CSS_SELECTOR, 'div.a-spacing-none > span.savingsPercentage').text.strip()
        # img
        img = driver.find_element(By.XPATH, '//div[@id="imgTagWrapperId"]/img').get_attribute("src")

        # CSVに追記
        with open('amazon_products.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title, original_price, discount_price, discount_rate, img])

        print("[INFO] 商品情報をCSVに書き込みました:", title)

    except Exception as e:
        print("[ERROR] 商品情報の取得に失敗しました:", e)

# WebDriverを閉じる
driver.quit()
