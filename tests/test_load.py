
# External
import datetime
from decimal import Decimal

# Project
from pipeline.load import insert_weather_data_batch
from config.database import get_db_connection


def test_insert_weather_data_batch():
   
    # Sample data for testing
    transformed_station_data = {
        'station_id': '002PG',
        'station_name': 'Reservation Road',
        'station_timezone': 'America/Los_Angeles',
        'latitude': Decimal('36.63359'),
        'longitude': Decimal('-121.69699')
    }
    transformed_observations = [
        {
            'observation_timestamp': datetime.datetime(2024, 10, 25, 11, 50),
            'temperature': Decimal('9.26'),
            'wind_speed': Decimal('2.12'),
            'humidity': Decimal('67.4')
        }
    ]
    
    # Run the function to insert data
    test_db = get_db_connection() 
    insert_weather_data_batch(test_db, transformed_station_data, transformed_observations)
    
    # Query the database to verify insertion
    test_db = get_db_connection() 
    with test_db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM weather_data WHERE station_id = %s;", 
            (transformed_station_data['station_id'],)
        )
        result = cursor.fetchall()
        test_db.close()

    # Expected data to match the inserted data
    expected_result = (
        transformed_station_data['station_id'],
        transformed_station_data['station_name'],
        transformed_station_data['station_timezone'],
        transformed_station_data['latitude'],
        transformed_station_data['longitude'],
        transformed_observations[0]['observation_timestamp'],
        transformed_observations[0]['temperature'],
        transformed_observations[0]['wind_speed'],
        transformed_observations[0]['humidity']
    )
    
    # Assert that the result matches expected data
    assert expected_result in result, f"Expected {expected_result} not in database"