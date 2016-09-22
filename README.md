#Project: Wrangling London OpenStreetMap Data
In this project, I downloaded an XML OpenStreetMap dataset and used data wrangling techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity to clean the OSM data.

I downloaded the data in XML, processed it into JSON and imported it into a MongoDB database. Once in the database, I ran queries to explore the data and understand it. Finally, I communicated my findings with a PDF document about the data.

##Required Libraries and Dependencies
### Language
* [Python][1] 

###Installations
* [MongoDB][2] 
* [PyMongo][3]

##How to Run Project
1. Download London dataset from OpenStreetMap website.
2. Move dataset into project root directory
3. Using terminal, navigate to the project root directory.
4. In the terminal, type **python data.py** to create .json file (may have to audit data to see if parsed data is correct).
5. In terminal, type **mongod** to launch mongodb.
6. Import json document into mongo using following command: **mongoimport -d <databaseName> -c <collectionName> --file <filename>.json**
7. Run **data_overview.py** to do queries on data in mongodb database.
8. To log out of mongodb database, enter ctrl-c twice in terminal.


[1]: http://python.org
[2]: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
[3]: http://api.mongodb.com/python/current/installation.html

##Miscellaneous
[Importing json into MongoDB][https://discussions.udacity.com/t/import-json-into-mongodb-project3/158051/4]
[Performing queries on MongoDB database][https://discussions.udacity.com/t/uploading-json-file-and-performing-query-in-mongodb/42777/4]
###Example Queries in terminal for mongodb
1. Enter mongo shell using **mongo** command in terminal
* Set Database: **use osm**
* col = db.ldn
* Number of documents in db: **col.find().count()**
* Most active user: **col.aggregate([{"$group":{ "_id":"$created.user", "count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":10}]).pretty()**