import pymongo
import dns # required for connecting with SRV
from bson import json_util
import traceback

from scrapf import scrap_data


def connection():
     try:
          client = pymongo.MongoClient("mongodb+srv://superchain:superchain@cluster0.clwzb.mongodb.net/test")
          # print(client.list_database_names())
     except Exception as e:
          traceback.print_tb(e.__traceback__)
          print(e)
     db = client['products']
     db = db['sd_uk']
     return db



def dataBase(url,db,driver):
          # print(db,"  ",url)

          data = scrap_data(url,driver)
          try:
               check = not bool(data)
               if check:
                    print(check)
                    raise Exception("Null Data")
               try:
                    db.insert_one(data)
                    print("inserting")
                    print("inserted")
                    # return "inserted"
               except pymongo.errors.DuplicateKeyError as e:
                    print("Updating records, details are already exist", e)
                    db.update({"_id": data['_id']},
                              {"$set": {"price": data['price'], "stock": data['stock']
                                   ,"rating": data["rating"],'rootprice': data['rootprice'],"lastupdate":data['lastupdate']}})
                    print("Updated")

          except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print('Error is ', e)
                    print("not inserted")



# dataBase("https://www.superdrug.com/Skin/Face-Skin-Care/Cleansers/Cleansing-Milks/Anne-French-Cleansing-Milk-200ml/p/26989",connection(),driver)

