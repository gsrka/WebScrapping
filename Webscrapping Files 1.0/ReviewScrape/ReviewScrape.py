from lxml import html
import requests
import json
import AmazonConnector as amazon



def getReviewBySearchKey(search):
    search = search
    reviewDict = amazon.getReviewURLArray(search)
    valid = 200
    reviewData = {}

    for reviewAsin in reviewDict:
        #fetch iframeURL and fetch all review page url
        print("PRODUCT[ASIN]: " + reviewAsin)
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
        for reviewid in reviewids:
            #TODO: CREATE TEMP TABLE FOR MONGODB
            review_date = allreviewtree.xpath(".//div[contains(@id, 'customer_review-" + reviewid + "')]//span[@data-hook='review-date']/text()")[0]
            title = allreviewtree.xpath(".//div[contains(@id, 'customer_review-" + reviewid + "')]//a[@data-hook='review-title']/text()")[0]
            star_rating = allreviewtree.xpath(".//div[contains(@id, 'customer_review-" + reviewid + "')]//i[contains(@data-hook, 'review-star-rating')]//span/text()")[0].split(" ")[0]
            author = allreviewtree.xpath(".//div[contains(@id, 'customer_review-" + reviewid + "')]//a[@data-hook='review-author']/text()")[0]
            review_text = allreviewtree.xpath(".//div[contains(@id, 'customer_review-"+ reviewid +"')]//span[@data-hook='review-body']/text()")[0]

            reviewData[reviewAsin].append({'ReviewId':reviewid,
                                           'ReviewDate':review_date,
                                           'ReviewTitle': title,
                                           'StarRating': star_rating,
                                           'ReviewAuthor': author,
                                           'ReviewText': review_text
                                           })
            print(reviewData)

    return reviewData

data = getReviewBySearchKey("java")
print(data)
print(len(data))