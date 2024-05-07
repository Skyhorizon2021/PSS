from pymongo import MongoClient

client = MongoClient()
host = 'localhost'
port_number = 27017
client = MongoClient(host,port_number)

mydb = client['Schedule']
mycollection = mydb['Schedule']