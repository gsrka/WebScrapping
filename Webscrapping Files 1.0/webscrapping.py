import amazonproduct
import socket
#import json
#import os
from selenium import webdriver

api = amazonproduct.API(cfg='F:/MIS/Amazon scrapping/.amazon-product-api', locale="us")
items = api.item_search('Books', Title="A Mind For Numbers", paginate=False)
print items

path = r"F:\MIS\Amazon scrapping\chromedriver_win32 (1)\chromedriver.exe"


for item in items.Items.Item.ItemLinks.ItemLink:
    if item.Description == "All Customer Reviews":
        #print item.URL
        url = item.URL

print(url)
socket.setdefaulttimeout(60)
driver = webdriver.Chrome(path)

url_string = str(url)
url_string = "http" + url_string[5:]
#url_string.replace("https", "http")
print(url_string)
driver.get(url_string)

#PRODUCT_NAME = driver.find_element_by_xpath('/div/div[contains(@class,"product-title")]/h1/a[@data-hook="product-link"]/text()')
XPATH_PRODUCT_NAME = '//div[@class="a-row product-title"]/h1[@role="link"]/a[@data-hook="product-link"]'
PRODUCT_NAME = driver.find_element_by_xpath(XPATH_PRODUCT_NAME)
print(PRODUCT_NAME.text)