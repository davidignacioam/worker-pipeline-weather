
# External
from psycopg2 import OperationalError

# Project
from config.database import get_db_connection


def test_get_db_connection():
    try:
        conn = get_db_connection()
        assert conn is not None
        conn.close()
    except OperationalError:
        assert False, "Database connection failed"