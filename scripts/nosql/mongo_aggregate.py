from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "healthcare_nosql"
COLLECTION_NAME = "appointments"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("\nTotal appointments per neighborhood:")
pipeline1 = [
    {"$group": {"_id": "$neighborhood", "totalAppointments": {"$sum": 1}}},
    {"$sort": {"totalAppointments": -1}},
]
for doc in collection.aggregate(pipeline1):
    print(doc)

print("\nTop 5 doctors by number of patients:")
pipeline2 = [
    {"$group": {"_id": "$doctor_id", "uniquePatients": {"$addToSet": "$patient_id"}}},
    {"$project": {"doctor_id": "$_id", "numPatients": {"$size": "$uniquePatients"}}},
    {"$sort": {"numPatients": -1}},
    {"$limit": 5},
]
for doc in collection.aggregate(pipeline2):
    print(doc)

print("\nNo-show rate by age group:")
pipeline3 = [
    {
        "$group": {
            "_id": "$age_group",
            "total": {"$sum": 1},
            "noShows": {"$sum": {"$cond": [{"$eq": ["$attended", False]}, 1, 0]}},
        }
    },
    {
        "$project": {
            "age_group": "$_id",
            "no_show_rate": {
                "$round": [{"$multiply": [{"$divide": ["$noShows", "$total"]}, 100]}, 2]
            },
        }
    },
    {"$sort": {"no_show_rate": -1}},
]
for doc in collection.aggregate(pipeline3):
    print(doc)
