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
# 検索窓 
Word = "冷蔵庫"
driver.find_element(By.ID, "twotabsearchtextbox").send_keys(Word)
sleep(1)
driver.find_element(By.ID,"nav-search-submit-button").click()
# 商品URLの取得 
URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")

for URL in URLS:
    URL = URL.get_attribute("href")
    print("[INFO] URL :", URL)
    HREFS.append(URL)

# CSVファイルを作成してヘッダーを書き込む
csv_filename = "amazon_products.csv"
headers = ["タイトル", "割引価格", "割引率", "画像URL"]
with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    # 商品詳細の取得
    for HREF in HREFS:
        driver.get(HREF)
        # title
        title = driver.find_element(By.ID, "productTitle").text
        # discount_price 
        discount_price = driver.find_element(By.CSS_SELECTOR, 'div.aok-align-center > span > span > span.a-price-whole').text
        # discount_rate
        discount_rate = driver.find_element(By.CSS_SELECTOR, 'div.a-spacing-none > span.savingsPercentage').text
        # img
        img = driver.find_element(By.XPATH, '//div[@id="imgTagWrapperId"]/img').get_attribute("src")

        # データをCSVに書き込む
        row_data = [title, discount_price, discount_rate, img]
        writer.writerow(row_data)

# ブラウザを閉じる
driver.quit()

print(f"[INFO] データは {csv_filename} に書き込まれました")

 