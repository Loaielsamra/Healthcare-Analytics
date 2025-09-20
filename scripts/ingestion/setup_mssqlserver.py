import os
import pandas as pd
import yaml
from sqlalchemy import create_engine, text

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SQL_HOST = config["sqlserver"]["host"]
SQL_PORT = config["sqlserver"]["port"]
DB_NAME = config["sqlserver"]["database"]
DRIVER = config["sqlserver"]["driver"]

RAW_DB_URL = f"mssql+pyodbc://@{SQL_HOST}/master?driver={DRIVER.replace(' ', '+')}&trusted_connection=yes"

HEALTHCARE_DB_URL = f"mssql+pyodbc://@{SQL_HOST}/{DB_NAME}?driver={DRIVER.replace(' ', '+')}&trusted_connection=yes"

SCHEMA_FILE = "scripts/sql/schema.sql"
DATA_PATH = "data/clean"


def create_database():
    """Create SQL Server database (if not exists)."""
    engine = create_engine(RAW_DB_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        try:
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database {DB_NAME} created")
        except Exception as e:
            print(f"Database {DB_NAME} may already exist: {e}")


def run_schema():
    """Run schema.sql on the target database."""
    engine = create_engine(HEALTHCARE_DB_URL)
    with engine.connect() as conn:
        with open(SCHEMA_FILE, "r") as f:
            schema_sql = f.read()
            conn.execute(text(schema_sql))
            print("Schema created")


def load_csvs():
    """Load patients, doctors, appointments CSVs into SQL Server tables."""
    engine = create_engine(HEALTHCARE_DB_URL)
    conn = engine.raw_connection()

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
    load_csvs()
