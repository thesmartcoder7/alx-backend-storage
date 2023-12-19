#!/usr/bin/env python3

""""
Python script that provides some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017')
    collection = client.logs.nginx

    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}".format(method, collection.count_documents({"method": method})))
    print("{} status check".format(collection.count_documents({"path": "/status"})))
