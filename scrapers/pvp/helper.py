from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://Tuasta:Aurnowac9737%23@116.203.206.106:27017/admin")

# Access the specific database and collection
db = client.data
collection = db.pvp

# Retrieve all documents from the collection
documents = collection.find()

# Convert ObjectId to string for JSON serialization and print the documents


# Print all retrieved documents
for document in documents:
    
    collection.delete_many({'numero_inserzione': document['numero_inserzione']})
    document['numero_inserzione'] = int(document['numero_inserzione'])
    collection.insert_one(document)
