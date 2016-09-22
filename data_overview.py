#!/usr/bin/env python

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def num_of_docs():
	return db.ldn.find().count() ## db.collectionname

if __name__ == "__main__":
    db = get_db('osm')
    print num_of_docs()
