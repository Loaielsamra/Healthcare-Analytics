import yaml
from sqlalchemy import create_engine, text

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

SQL_HOST = config["DW"]["host"]
SQL_PORT = config["DW"]["port"]
DB_NAME = config["DW"]["database"]
DRIVER = config["DW"]["driver"]

RAW_DB_URL = f"mssql+pyodbc://@{SQL_HOST}/master?driver={DRIVER.replace(' ', '+')}&trusted_connection=yes"
HEALTHCARE_DB_URL = f"mssql+pyodbc://@{SQL_HOST}/{DB_NAME}?driver={DRIVER.replace(' ', '+')}&trusted_connection=yes"
SCHEMA_FILE = "scripts/sql/DW_Schema.sql"


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
            print("Schema created")


if __name__ == "__main__":
    create_database()
    run_schema()
