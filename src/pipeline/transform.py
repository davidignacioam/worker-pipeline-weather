
# Base
import logging
from datetime import datetime

# Project
from config.config import SERVICE


logger = logging.getLogger(SERVICE)


def transform_station_data(station_data: dict) -> dict:
   """
   Summary:
      Transform station data to a format suitable for the database.
   Args:
      station_data (dict): The station data to transform.
   Returns:
      dict: The transformed station data.
   """
   try:
      return {
         'station_id': station_data['properties']['stationIdentifier'],
         'station_name': station_data['properties']['name'],
         'station_timezone': station_data['properties']['timeZone'],
         'latitude': station_data['geometry']['coordinates'][1],
         'longitude': station_data['geometry']['coordinates'][0]
      }
   except KeyError as e:
      logger.error(f"Error transforming STATION data: {e}")
      return {}

def transform_observation(observation: list) -> dict:
   """
   Summary:
      Transform observation data to a format suitable for the database.
   Args:
      observation (list): The observation data to transform.
   Returns:
      dict: The transformed observation data.
   """
   try:
      properties = observation['properties']
      temperature = properties['temperature']['value']
      wind_speed = properties['windSpeed']['value']
      humidity = properties['relativeHumidity']['value']
      return {
         'observation_timestamp': datetime.fromisoformat(properties['timestamp'].replace("Z", "")),
         'temperature': round(temperature, 2) if temperature is not None else None,
         'wind_speed': round(wind_speed, 2) if wind_speed is not None else None,
         'humidity': round(humidity, 2) if humidity is not None else None
      }
   except KeyError as e:
      logger.error(f"Error transforming OBSERVATION data: {e}")
      return {}
   

def transform_data(station_data: dict, observations: list) -> tuple:
   
   # Validate the input data
   if not station_data or not observations:
      logger.error("No data to Insert")
      return {}, []
   
   # Transform the data in Station and Observations
   transformed_station_data = transform_station_data(station_data)
   transformed_observations = [transform_observation(obs) for obs in observations]
   if not transformed_station_data or not transformed_observations:
      logger.error("No transformed data to insert")
      return {}, []
   
   # Log the transformation results
   logger.info(f"Total Transformed OBSERVATIONS: {len(transformed_observations)}")
   logger.info(f"Total Transformed STATION data: {len(transformed_station_data)}")  
   return transformed_station_data, transformed_observations
   
