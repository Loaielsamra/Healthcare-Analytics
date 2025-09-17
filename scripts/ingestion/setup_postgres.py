import os
import pandas as pd
import yaml
from sqlalchemy import create_engine, text

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

PG_USER = config["postgres"]["user"]
PG_PASSWORD = config["postgres"]["password"]
PG_HOST = config["postgres"]["host"]
PG_PORT = config["postgres"]["port"]
DB_NAME = config["postgres"]["database"]

RAW_DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/postgres"
HEALTHCARE_DB_URL = (
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"
)

SCHEMA_FILE = "scripts/sql/schema.sql"
DATA_PATH = "data/clean"


def create_database():
    engine = create_engine(RAW_DB_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        try:
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database {DB_NAME} created")
        except Exception as e:
            print(e)
            raise


def run_schema():
    engine = create_engine(HEALTHCARE_DB_URL)
    with engine.connect() as conn:
        with open(SCHEMA_FILE, "r") as f:
            schema_sql = f.read()
            conn.execute(text(schema_sql))
            print(" Schema created")


def load_csvs():
    engine = create_engine(HEALTHCARE_DB_URL)

    conn = engine.connect()

    patients = pd.read_csv(os.path.join(DATA_PATH, "patients.csv"))
    doctors = pd.read_csv(os.path.join(DATA_PATH, "doctors.csv"))
    appointments = pd.read_csv(os.path.join(DATA_PATH, "appointments.csv"))

    patients.to_sql("patients", conn, if_exists="append", index=False)
    print(f"Loaded {len(patients)} patients")

    doctors.to_sql("doctors", conn, if_exists="append", index=False)
    print(f"Loaded {len(doctors)} doctors")

    appointments.to_sql("appointments", conn, if_exists="append", index=False)
    print(f"Loaded {len(appointments)} appointments")


if __name__ == "__main__":
    create_database()
    run_schema()
    # load_csvs()
