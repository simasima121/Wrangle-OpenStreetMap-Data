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

def num_of_nodes_ways(s):
	"""
	Returns number of nodes or ways
	"""
	return db.ldn.find({"type":s}).count()

def num_of_amenity(s):
	"""
	Returns number of amenity in nodes
	"""
	count = 0
	for ele in db.ldn.find({"type":"node","amenity":s}):
		count += 1
	return count

def most_active_users():
	"""
	Returns 5 most active users
	"""
	pipeline = [{"$group":{ "_id":"$created.user", "count":{"$sum":1}}},
				{"$sort":{"count":-1}},
				{"$limit":5}]

	return [doc for doc in db.ldn.aggregate(pipeline)]

if __name__ == "__main__":
    db = get_db('osm')
    import pprint

    print "Number of documents: ", num_of_docs()
    print "Number of unique users: ", num_of_unique_users()

    print "Number of nodes: ", num_of_nodes_ways("node")
    print "Number of ways: ", num_of_nodes_ways("way")

    print "Number of cafes: ", num_of_amenity("cafe")
    print "Number of pubs: ", num_of_amenity("pub")
    print "Number of schools: ", num_of_amenity("school")

    print "5 Most Active Users: "
    pprint.pprint(most_active_users())
