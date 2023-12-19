#!/usr/bin/env python3

"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs
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

    print("IPs:")
    ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in ips:
        print("\t{}: {}".format(ip.get("_id"), ip.get("count")))
