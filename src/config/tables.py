
# Base
import logging

# Project
from config.config import CREATE_TABLE_SQL, SERVICE
from config.database import get_db_connection


logger = logging.getLogger(SERVICE)


def create_weather_data_table() -> None:
    """
    Summary:
        Creates the weather_data table in PostgreSQL if it doesn't exist.
    """
    try:
        
        # Get a connection to the database. If the connection fails, the function will return None.
        conn = get_db_connection()
        if conn is None:
            logger.error("Failed to establish a database connection.")
            return

        # Create the table. If the table already exists, the operation will not raise an error.
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
            conn.commit()
            logger.info("Table 'weather_data' created successfully or already exists.")
    
    except Exception as e:
        logger.error(f"Error creating the weather_data table: {e}")
        raise
    
    finally:
        # Ensure the connection is closed after the operation
        if conn:
            conn.close()
            logger.info("Database connection closed.")

# Create the table
create_weather_data_table()