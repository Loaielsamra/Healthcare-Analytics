import os
import json
import pandas as pd
from pymongo import MongoClient

DATA_PATH = "data/clean"
NOSQL_PATH = "data/nosql"
APPOINTMENTS_JSON = os.path.join(NOSQL_PATH, "appointments.json")

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "healthcare_nosql"
COLLECTION_NAME = "appointments"


def export_and_merge():
    """Merge patients into appointments and export JSON for MongoDB."""
    os.makedirs(NOSQL_PATH, exist_ok=True)

    patients = pd.read_csv(os.path.join(DATA_PATH, "patients.csv"))
    appointments = pd.read_csv(os.path.join(DATA_PATH, "appointments.csv"))

    # Merge neighborhood + age_group into appointments
    appointments = appointments.merge(
        patients[["patient_id", "age_group", "neighborhood"]],
        on="patient_id",
        how="left",
    )

    appointments.to_json(APPOINTMENTS_JSON, orient="records", lines=True)
    print(f"Exported {len(appointments)} records to {APPOINTMENTS_JSON}")


def load_into_mongodb():
    """Load exported JSON into MongoDB collection."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Drop existing collection for fresh load
    collection.drop()

    with open(APPOINTMENTS_JSON, "r", encoding="utf-8") as f:
        docs = [json.loads(line) for line in f]

    collection.insert_many(docs)
    print(f"Inserted {len(docs)} documents into {DB_NAME}.{COLLECTION_NAME}")


if __name__ == "__main__":
    export_and_merge()
    load_into_mongodb()
