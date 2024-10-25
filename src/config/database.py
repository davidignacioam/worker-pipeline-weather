
# Base
import logging

# External
import psycopg2

# Project
from config.config import (
    POSTGRESQL_SERVER,
    POSTGRESQL_DATABASE,
    POSTGRESQL_USER,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_PORT,
    SERVICE
)


logger = logging.getLogger(SERVICE)


INSERT_QUERY = '''
    INSERT INTO weather_data (
        station_id, 
        station_name, 
        station_timezone, 
        latitude, longitude, 
        observation_timestamp, 
        temperature, 
        wind_speed, 
        humidity
    )
    VALUES %s
    ON CONFLICT (station_id, observation_timestamp) DO NOTHING;
'''

CREATE_TABLE_SQL = '''
    CREATE TABLE IF NOT EXISTS weather_data (
        station_id VARCHAR(10),
        station_name VARCHAR(100),
        station_timezone VARCHAR(50),
        latitude DECIMAL(8, 6),
        longitude DECIMAL(9, 6),
        observation_timestamp TIMESTAMP,
        temperature DECIMAL(5, 2),
        wind_speed DECIMAL(5, 2),
        humidity DECIMAL(5, 2),
        PRIMARY KEY (station_id, observation_timestamp)
    );
'''

def get_db_connection():
    """
    Summary:
        Set up a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host = POSTGRESQL_SERVER,
            port = POSTGRESQL_PORT,
            database = POSTGRESQL_DATABASE,
            user = POSTGRESQL_USER,
            password = POSTGRESQL_PASSWORD
        )
        logger.info(f"Database connection established")
        return conn
    
    except psycopg2.DatabaseError as e:
        logger.error(f"Database connection error: {e}")
        raise