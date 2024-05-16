import pymongo
import json

class Schedule:
    def loadData(filename):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        with open("Resources//Set1.json") as file:
            file_data = json.load(file)

        mycol.insert_many(file_data)
    
    def getData():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

<<<<<<< HEAD
        schedule = []

        x = mycol.find()
        for doc in x:
            del doc['_id']
            schedule.append(doc)
        return schedule
Schedule.getData()
=======
        x = mycol.find_one()
        del x['_id']
        return x

#Schedule.loadData('Resources//db_example.json')
>>>>>>> 89c4ba0ae5542ab91c3b7f601fb8204ff06eebbc
