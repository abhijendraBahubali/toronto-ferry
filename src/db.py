import os

import psycopg
from dotenv import load_dotenv

# Load variables from the .env file (same one used by docker-compose.yml)
load_dotenv()

# Connection details for the Postgres container defined in docker-compose.yml.
# The container publishes Postgres on localhost:5432; credentials come from .env.
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT")),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def get_connection() -> psycopg.Connection:
    """Open a new connection to the Postgres database."""
    return psycopg.connect(**DB_CONFIG)


if __name__ == "__main__":
    # Quick connectivity check: python -m src.db
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(cur.fetchone()[0])
