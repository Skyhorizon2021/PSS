import pymongo
import json

class Schedule:
    def loadData(filename):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        with open(filename) as file:
            file_data = json.load(file)

        mycol.insert_one(file_data)
    
    def getData():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        x = mycol.find_one()
        del x['_id']
        return x
