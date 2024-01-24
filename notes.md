# What is it?
- A document-oriented database
- A no(t-only)-SQL database
- Based on a binary version of JSON (called BSON)

# Installation
Via docker
1. Get Docker image https://hub.docker.com/_/mongo/
2. Create a docker-compose.yml file in the top level directory of the project
3. `docker compose up -d`

# How to use it
1. Start the docker container
2. To get into the (bash) shell of the docker instance  ```docker exec -it mongo_image_name bash```
3. To get into the mongo shell on the docker instance ```docker exec -it mongo_image_name mongosh```

# Getting data into the DB
If using docker, you'll need to get data files onto the docker container. Following [this](https://stackoverflow.com/questions/49895447/i-want-to-execute-mongoimport-on-a-docker-container) StackExchange answer:
```bash
docker cp xxx.json <container-name-or-id>:/tmp/xxx.json
```
Then
``` bash
docker exec <container-name-or-id> mongoimport -d <db-name> -c <c-name> --file /tmp/xxx.json
```

# Select data

Let's look at our first document with the command below:

```shell
db.zips.findOne()
```

However, we have nothing. Let's unpack the query. 
The keyword `db` refers to the current **database**. 
The following is the **collection name**, in this case the `zips` collection. 
Finally, have the function being called, here the `findOne` function, which returns one document from the collection.

This returns no results if there are no documents in the database.

To change database we use the `use` command

``` shell
use {database_name}
```

We can import json data from a file "grades.json" into a mongo collection "grades" in the database "sample" (from ordinary shell) as follows
``` shell
mongoimport -d sample -c grades --file grades.json
```
## Short reference to finding documents in a MongoDB database
``` mongosh
db.{collection_name}.findOne() # Get a random entry in collection
db.{collection_name}.find() # Get all entries in collection
db.{collection_name}.findOne({'Attribute':'Value'}) # Get an entry matching where the attribute `Attribute` has a value `Value` 
```

# Insert data

``` mongosh
db.zips.insert(
  {"city":"Paris","state":"France"}
  )
```

Note that the unique key is ``_id``
``` mongosh
>  db.zips.find({'city':'Paris'})
RESULT:
[
  {
    _id: ObjectId('65ad11cb28471e889d64f4c6'),
    city: 'Paris',
    state: 'France'
  }
]


```

## Insert multiple records:
```mongosh
db.zips.insertMany([
  {"city":"Paris","state":"France"},
  {"city": "Courbevoie","state":"France"}
  ])
```

# Update entries
```mongosh
db.zips.updateOne({"city":"BREMEN"},{$set : {"state":"France"}})
```

Can also use `updateMany`

# Delete entries

``` mongosh
db.grades.updateOne(
  {"_id":ObjectId("56d5f7eb604eb380b0d8d9c8")},
  {$push: {"scores" :  {"exam": "quizz" , "score": 100.0}}}
  )
```

# Delete a collection

``` mongosh
db.zips.drop()
```

# Sorting 
```shell
db.grades.find().sort({"student_id":-1})
```

# Projection

```
db.zips.find({"state":"TX"},{"pop":1})
```
By associating the value 1 to the key `pop` in the second argument to find, we tell MongoDB to **include** only the number of inhabitants in our results. 
We can **exclude** the key `pop` by using {`pop`: 0} as the second argument to the find function. This is **projection**, simplifying or expanding the view that we have of data in the database, based on what we are interested in.
```
db.zips.find({"state": "TX"},{"pop":0})
```


# Data Modelling for Documents

Structure of data affects performance

It's common with relational databases to denormalize data, for instance by putting it in a star schema

To determine the appropriate structure for data, you must know what data the end application is going to need, and what types of query it will need to do most frequently and with best performance.

Data modelling is going to be iterative
![[Data modelling workflow diagram]](img/data_modelling_workflow.png)

Step 1: Determine the app functionalities / use-case
- What questions do we want to answer? (e.g. be able to tell the density of forest fires in the Amazon)
- What things do we want to do? (e.g. view fire events on a map, including a polygon of the affected region, showing area and size)
- Data size (MBs, or PBs, thousands or billions of records, how many dimensions?)
- Data format JSON/XML/audio/mixed

Step 2: Define entities and relations
- e.g. in the case of the fire monitoring application - a region might be an entity, and so might a forest fire event. The relation might be that fires can be associated with certain regions
- Here's some example data for fire_events. It comes in a JSON format:
```
{'fire_events':
[
{'date_observed':'2024-01-10',
'date_extinguished':null,
'region':
	{'id':'reg021321',
	'name':'Amazon River West Region A'
	},
'area':{
	'maximum_extent':1000,
	'current_area':100,
	'polygon':'(0.752691110661913, 0.948158571633034), (0.7790276993942304, 0.05437135270534656),(0.633385213909564, 0.7365967958574935)'}
}
]}
```

Are the relationships `1-1` (One to One), `1-N` (One to Many) and `N-N` (Many to Many)?
- In this example, *Forest fire event - to region* is likely a `N-1` relation

Step 3: Finalize the data model for each collection
- Is the structure of the documents suitable for our usage? 
- Do we have too many fields?
- Are there some fields we may want to compute, to make querying the data fast enough to serve the end use?

# GUIs for MongoDB

Atlas is most common

MongoExpress another option, but only for development environments# What is it?
- A document-oriented database
- A no(t-only)-SQL database
- Based on a binary version of JSON (called BSON)

# Installation
Via docker
1. Get Docker image https://hub.docker.com/_/mongo/
 2. Create a docker-compose.yml file in the top level directory of the project
 4. `docker compose up -d`

# How to use it
1. Start the docker container
2. To get into the (bash) shell of the docker instance  ```docker exec -it mongo_image_name bash```
3. To get into the mongo shell on the docker instance ```docker exec -it mongo_image_name mongosh```

# Getting data into the DB
If using docker, you'll need to get data files onto the docker container. Following [this](https://stackoverflow.com/questions/49895447/i-want-to-execute-mongoimport-on-a-docker-container) StackExchange answer:
```bash
docker cp xxx.json <container-name-or-id>:/tmp/xxx.json
```
Then
``` bash
docker exec <container-name-or-id> mongoimport -d <db-name> -c <c-name> --file /tmp/xxx.json
```

# Select data

Let's look at our first document with the command below:

```shell
db.zips.findOne()
```

However, we have nothing. Let's unpack the query. The keyword `db` refers to the current database. In this case, it is `test`. Next, the collection name follows the word `db`, this will mean that we are selecting the `zips` collection. Finally, we will call our functions at the end, here the `findOne` function returns a document from the collection.

Here we have no documents because we are not in the right database.

``` shell
use {database_name}
```
Import json data from a file "grades.json" into a mongo collection "grades" in the database "sample" (from ordinary shell)
``` shell
mongoimport -d sample -c grades --file grades.json
```
### Short reference
``` mongosh
db.{collection_name}.findOne() # Get a random entry in collection
db.{collection_name}.find() # Get all entries in collection
db.{collection_name}.findOne({'Attribute':'Value'}) # Get an entry matching where the attribute `Attribute` has a value `Value` 
```

# Insert data

``` mongosh
db.zips.insert(
  {"city":"Paris","state":"France"}
  )
```

Note that the unique key is ``_id``
``` mongosh
>  db.zips.find({'city':'Paris'})
RESULT:
[
  {
    _id: ObjectId('65ad11cb28471e889d64f4c6'),
    city: 'Paris',
    state: 'France'
  }
]


```

Insert multiple records:
```mongosh
db.zips.insertMany([
  {"city":"Paris","state":"France"},
  {"city": "Courbevoie","state":"France"}
  ])
```

# Update entries
```mongosh
db.zips.updateOne({"city":"BREMEN"},{$set : {"state":"France"}})
```

Can also use `updateMany`

# Delete entries

``` mongosh
db.grades.updateOne(
  {"_id":ObjectId("56d5f7eb604eb380b0d8d9c8")},
  {$push: {"scores" :  {"exam": "quizz" , "score": 100.0}}}
  )
```

# Delete a collection

``` mongosh
db.zips.drop()
```

# Sorting 
```shell
db.grades.find().sort({"student_id":-1})
```

# Projection

```
db.zips.find({"state":"TX"},{"pop":1})
```
By associating the value 1 to the key `pop`, we tell MongoDB to **include** only the number of inhabitants in our results. It is possible to do the opposite operation and **exclude** the key `pop` from our results, we will have to associate the value 0 to `pop`.
```
db.zips.find({"state": "TX"},{"pop":0})
```


# Data Modelling for Documents

Structure of data affects performance

It's common with relational databases to denormalize data, for instance by putting it in a star schema

To determine the appropriate structure for data, you must know what data the end application is going to need, and what types of query it will need to do most frequently and with best performance.

Data modelling is going to be iterative
![[data_modelling_workflow.png]]

Step 1: Determine the app functionalities / use-case
- What questions do we want to answer? (e.g. be able to tell the density of forest fires in the Amazon)
- What things do we want to do? (e.g. view fire events on a map, including a polygon of the affected region, showing area and size)
- Data size (MBs, or PBs, thousands or billions of records, how many dimensions?)
- Data format JSON/XML/audio/mixed

Step 2: Define entities and relations
- e.g. in the case of the fire monitoring application - a region might be an entity, and so might a forest fire event. The relation might be that fires can be associated with certain regions
- Here's some example data for fire_events. It comes in a JSON format:
```
{'fire_events':
[
{'date_observed':'2024-01-10',
'date_extinguished':null,
'region':
	{'id':'reg021321',
	'name':'Amazon River West Region A'
	},
'area':{
	'maximum_extent':1000,
	'current_area':100,
	'polygon':'(0.752691110661913, 0.948158571633034), (0.7790276993942304, 0.05437135270534656),(0.633385213909564, 0.7365967958574935)'}
}
]}
```

Are the relationships `1-1` (One to One), `1-N` (One to Many) and `N-N` (Many to Many)?
- In this example, *Forest fire event - to region* is an `N-1` relation

Step 3: Finalize the data model for each collection
- Is the structure of the documents suitable for our usage? 
- Do we have too many fields?
- Are there some fields we may want to compute, to make querying the data fast enough to serve the end use?

# GUIs for MongoDB

Atlas is most common

MongoExpress another option, but only for development environments
