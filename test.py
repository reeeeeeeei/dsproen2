import pandas as pd
import sqlite3
import requests
import time
from selenium import webdriver

#driverオブジェクト生成
driver = webdriver.Chrome(executable_path = '/opt/win32/chromedriver.exe')
time.sllep(5)
