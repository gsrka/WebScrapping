from pymongo import MongoClient

client = MongoClient()
db = client.test

db.products.insert_one({"Product_id":"ASIN","Vendor_id":"Seller_Id","ProductName":"PName","ProductDescription":"PDesc","CategoryID":"Category","Sizes_Available":"","Colours_Available":"", "Vendor_Nmae":"Vname","Unit_Price":"Price",""});

db.reviewers.insert_one({"Reviewer_name":"Rname","ReviewerID":"","Verified":"","Products_reviewed":"","Verified_on":""});

db.reviews.insert_one({"_id":"ASIN","Review_Author":"","Review_Date":"October 20 2016","Review_id":"R156","Review_Text":"","Review_Title":"","Star_Rating":""})

client.close()