#!/usr/bin/env python

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def num_of_docs():
	return db.ldn.find().count() ## db.collectionname

def num_of_unique_users():
	# Call in mongoshell is col.distinct("created.user").length
	return len(db.ldn.distinct("created.user"))

def most_active_users(db):
	pipeline = [{"$group":{ "_id":"$created.user", "count":{"$sum":1}}},
				{"$sort":{"count":-1}},
				{"$limit":5}]

	return [doc for doc in db.ldn.aggregate(pipeline)]

if __name__ == "__main__":
    db = get_db('osm')
    import pprint

    print "Number of documents: ",num_of_docs()
    print "Number of unique users: ",num_of_unique_users()

    print "5 Most Active Users: "
    pprint.pprint(most_active_users(db))
