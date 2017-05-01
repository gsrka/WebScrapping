from lxml import html
import requests
import AmazonConnector as amazon
import json
import pymongo

connection = pymongo.MongoClient("mongodb://localhost:27017/");

db = connection.Products
p = db.electronic

def getProductBySearchKey(search):
    search = search
    productDict = amazon.getProductURLArray(search)
    valid = 200
    reviewData = {}
    count = 0
    for productAsin in productDict:
        #fetch iframeURL and fetch all review page url
        count += 1

        print("PRODUCT[ASIN]: " + productAsin)
        reviewData[productAsin] = []


        status_code = -1
        page = requests.get(productDict[productAsin])
        while(status_code != valid):                            #ensures page returns valid response
            page = requests.get(productDict[productAsin])         #fetches page from url
            status_code = page.status_code                      #fetches status_code for internal comparison

        tree = html.fromstring(page.content)

        productdescription = tree.xpath(".//div[@id='productDescription']//p/text()")
        if(len(productdescription) > 0):
            productdescription = productdescription[0].strip()
        else:
            productdescription = ""
        productDeatilsTable = tree.xpath(".//table[@id='productDetails_detailBullets_sections1']")
        if(len(productDeatilsTable) > 0):
            productAttributeRows = productDeatilsTable[0].xpath(".//tr")
            reviewData[productAsin].append({'Product Description':productdescription})
            rowdetails ={}
            for row in productAttributeRows:
                #rowdetails = {}
                th = row.xpath(".//th/text()")[0].strip()
                td = row.xpath(".//td/text()")[0].strip()
                rowdetails[th] = td
            print rowdetails
            p_id = p.insert(rowdetails)
            reviewData[productAsin].append(rowdetails)
            #print(reviewData[productAsin])
#            d = pandas.DataFrame.from_dict(reviewData, orient='columns')
#            print(d[productAsin])

    return reviewData
#    return d


data = getProductBySearchKey("iphone")

print(len(data))