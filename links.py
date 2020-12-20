import json
import time
import traceback

import requests
from bs4 import BeautifulSoup
import re
import threading
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from db import dataBase, connection

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
driver = webdriver.Chrome()
# driver1 = driver
url = "https://www.superdrug.com/sitemap.xml"
try:
#     page = requests.get(url, headers=headers)
#     # driver.get(url)
#     # page = driver.page_source
#     soup = BeautifulSoup(page.text, 'html.parser')
#     # lik = []
#     # code = []
    db = connection()
#     # dataBase("https://www.superdrug.com/Skin/Face-Skin-Care/Cleansers/Cleansing-Milks/Anne-French-Cleansing-Milk-200ml/p/26989",db,driver)
#     for link in soup.findAll('loc'):
#         if re.search(r'\/[p]\/[\d]+', link.text):
#                 # lik.append(link.text)
#                 # code.append(str(link.text.split('/')[-1]))
#                 # if len(lik)==2 :
#                 #     # t1 = threading.Thread(target=dataBase, args=(lik[0],db,driver))
#                 #     # t2 = threading.Thread(target=dataBase,args=(lik[1],db))
#                 #     # t1.start()
#                 #     # t2.start()
#                 #
#                 #     lik = []
#                 # else:
#                 #     continue
    with open('link.txt') as f:
        for line in f:
            print(line)
            time.sleep(5)
            dataBase(line,db,driver)

#
#                 # dataBase(link.text,db,driver)
#                 with open('link.txt', 'a') as f:
#                         f.write(f"{link.text}\n")
#         # else:
#         #     continue
#
#          # print("data",return_data)
# except requests.exceptions.HTTPError as errh:
#     print("Http Error:", errh)
# except requests.exceptions.ConnectionError as errc:
#     print("Error Connecting:", errc)
# except requests.exceptions.Timeout as errt:
#     print("Timeout Error:", errt)
# except requests.exceptions.RequestException as err:
#     print("OOps: Something Else", err)
except Exception as e:
     traceback.print_tb(e.__traceback__)
     print(e)
# driver.close()

#with open('link.txt') as f:
#    for line in f:
#        print(line)
#        time.sleep(5)
