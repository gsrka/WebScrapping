import amazonproduct

#CREATE CREDENTIAL FILE
# .amazon-product-api in home directory
# [Credentials]
#access_key = <your access key>
#secret_key = <your secret key>
#associate_tag = <your associate id>
api = amazonproduct.API(locale='us')

def searchItem(key):
    items = api.item_search('All', Keywords=key, ResponseGroup='ItemIds,ItemAttributes,Reviews')
    return items

def getReviewURLArray(key):
    dict = {};
    items = searchItem(key)
    for item in items:
        if(item.CustomerReviews.HasReviews):
            dict[item.ASIN] = item.CustomerReviews.IFrameURL
    return dict

def getProductURLArray(key):
    dict = {};
    items = searchItem(key)
    for item in items:
        dict[item.ASIN] = item.DetailPageURL
    return dict