from lxml import html
import requests
import AmazonConnector as amazon
import json


def getProductBySearchKey(search):
    search = search
    productDict = amazon.getProductURLArray(search)
    valid = 200
    reviewData = {}

    for productAsin in productDict:
        #fetch iframeURL and fetch all review page url
        print("PRODUCT[ASIN]: " + productAsin)
        reviewData[reviewAsin] = []

        status_code = -1
        page = requests.get(reviewDict[reviewAsin])
        while(status_code != valid):                            #ensures page returns valid response
            page = requests.get(reviewDict[reviewAsin])         #fetches page from url
            status_code = page.status_code                      #fetches status_code for internal comparison

        tree = html.fromstring(page.content)
        allreviewurl = tree.xpath(".//span[contains(@class, 'small')]//b//a/@href")

        #Fetch all reviews page content
        status_code = -1
        while(status_code != valid):
            allreviewpage = requests.get(allreviewurl[0])
            status_code = allreviewpage.status_code

        allreviewtree = html.fromstring(allreviewpage.content)
        reviewids = allreviewtree.xpath(".//div[contains(@class, 'a-section review')]/@id")