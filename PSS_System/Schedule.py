import pymongo
import json

class Schedule:
    def loadData():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        with open('db_example.json') as file:
            file_data = json.load(file)

        mycol.insert_one(file_data)
    
    def getData():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        x = mycol.find_one()
        return x
