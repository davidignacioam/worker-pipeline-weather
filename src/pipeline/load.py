
# Base
import logging

# External
import pandas as pd
from psycopg2.extras import execute_values
from psycopg2 import DatabaseError

# Project
from config.config import SERVICE
from config.database import get_db_connection, INSERT_QUERY


logger = logging.getLogger(SERVICE)


def get_weather_data() -> pd.DataFrame:
    try:
        conn = get_db_connection()
        query = "SELECT * FROM weather_data"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None


def insert_weather_data_batch(conn, station_data: dict, observations: list) -> None:
    """
    Summary:
        Insert weather data in batch mode. 
        If the combination of station_id and observation_timestamp already exists, it will not insert the duplicate.
    Args:
        conn: Database connection object.
        station_data (dict): Dictionary containing station metadata.
        observations (list): List of weather observations to insert.
    """
    try:
        
        # Validate the connection and input data
        if not conn:
            logger.error("Database connection is not established.")
            return None
        if not observations:
            logger.warning("No observations provided for insertion.")
            return None
        
        prev_weather_df = get_weather_data()
        with conn.cursor() as cursor:
            
            # Create a list of tuples for batch insert
            # Use execute_values to perform batch insertion
            data = [
                (
                    station_data['station_id'],
                    station_data['station_name'],
                    station_data['station_timezone'],
                    station_data['latitude'],
                    station_data['longitude'],
                    obs['observation_timestamp'],
                    obs['temperature'],
                    obs['wind_speed'],
                    obs['humidity']
                )
                for obs in observations
            ]
            execute_values(cursor, INSERT_QUERY, data)
            conn.commit()
            
            # Validate the insertion operation
            post_weather_df = get_weather_data()
            if prev_weather_df is not None and post_weather_df is not None:
                diff_len_pre_post = abs(prev_weather_df.shape[0] - post_weather_df.shape[0])
                if diff_len_pre_post == 0 and len(prev_weather_df) > 0:
                    logger.warning(f"TOTAL DUPLICATED data: Total of {len(data)} rows descarted. No new data inserted into 'weather_data' table for station ID {station_data['station_id']}.")
                elif len(data) > diff_len_pre_post:
                    logger.warning(f"PARTIAL DUPLICATED data: Successfully inserted {diff_len_pre_post} rows of {len(data) }into 'weather_data' table for station ID {station_data['station_id']}.") 
                else:
                    logger.info(f"Successfully inserted {diff_len_pre_post} rows into 'weather_data' table for station ID {station_data['station_id']}.")
            
    except DatabaseError as e:
        logger.error(f"Database error occurred while inserting weather data: {e}")
        conn.rollback()  # Rollback transaction in case of error
        raise
    
    except Exception as e:
        logger.error(f"An error occurred while inserting weather data: {e}")
        raise
    
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")


def load_data(station_data: dict, observations: list) -> None:
    """
    Summary:
        Load observations in batch mode into the database, avoiding duplicates.
    """
    try:
        # Insert data in a batch instead of inserting one observation at a time
        conn = get_db_connection()
        insert_weather_data_batch(conn, station_data, observations)

    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        raise    
    
    finally:
        conn.close()
        logging.info("Database connection closed")