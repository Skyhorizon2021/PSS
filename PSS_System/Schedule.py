import pymongo
import json

class Schedule:
    def loadData(filename):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        with open(filename) as file:
            file_data = json.load(file)

        mycol.insert_many(file_data)
    
    def getData():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        schedule = []

        x = mycol.find()
        for doc in x:
            del doc['_id']
            schedule.append(doc)
        return schedule


