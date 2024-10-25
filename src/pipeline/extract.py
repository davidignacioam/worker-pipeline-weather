
# Base
import logging
import time

# External
import requests

# Project
from config.config import (
    API_BACKOFF_FACTOR,
    API_BASE_URL, 
    API_RETRIES,  
    API_TIMEOUT,
    SERVICE
)


logger = logging.getLogger(SERVICE)


def get_station_data(station_id):
    """
    Summary:
        Fetch station data from the weather API.
    Args:
        station_id (str): The station ID for which to fetch data.
    Returns:
        dict: The station data.
    """
    
    station_url = f"{API_BASE_URL}/stations/{station_id}"
    
    for attempt in range(API_RETRIES):
        try:
            response = requests.get(station_url, timeout=10)
            response.raise_for_status()
            logger.info(f"Fetched STATION data for station ID {station_id}")
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching station data: {e}")
            
            if attempt < API_RETRIES - 1:
                # Exponential backoff
                sleep_time = API_BACKOFF_FACTOR ** attempt
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                raise


def get_observations(station_id):
    """
    Fetch observations from the weather API with retries and exponential backoff.

    Args:
        station_id (str): The station ID for which to fetch observations.
        retries (int): Number of retry attempts. Default is 3.
        backoff_factor (int): Factor to apply for exponential backoff (in seconds). Default is 2.

    Returns:
        list: The observations.
    """

    observations_url = f"{API_BASE_URL}/stations/{station_id}/observations"

    for attempt in range(API_RETRIES):
        try:
            response = requests.get(observations_url, timeout = API_TIMEOUT)
            response.raise_for_status()  # Raise an exception for non-200 responses
            logger.info(f"Fetched OBSERVATIONS for station ID {station_id}")
            return response.json()['features']

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching observations on attempt {attempt + 1}: {e}")
            
            if attempt < API_RETRIES - 1:
                # Exponential backoff
                sleep_time = API_BACKOFF_FACTOR ** attempt
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error(f"Failed to fetch observations after {API_RETRIES} attempts.")
                raise


def extract_data(station_id):
    """
    Fetch station data and observations from the weather API.

    Args:
        station_id (str): The station ID for which to fetch data.

    Returns:
        tuple: The station data and observations.
    """
    
    # Validate the input data
    if not station_id or not isinstance(station_id, str):
        logger.error("Invalid station ID provided.")
        return {}, []

    # Fetch the station data and observations
    station_data = get_station_data(station_id)
    observations = get_observations(station_id)
    return station_data, observations
   