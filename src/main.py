
from config.logger import LogConfig
from logging.config import dictConfig

from pipeline.extract import extract_data
from pipeline.transform import transform_data
from pipeline.load import load_data

dictConfig(LogConfig().dict())


station_id = "002PG" # Station ID Selected

def run_pipeline(station_id):
    
    station_data, observations = extract_data(station_id)
    
    transformed_station_data, transformed_observations = transform_data(station_data, observations)
    
    load_data(transformed_station_data, transformed_observations)


if __name__ == "__main__":
    run_pipeline(station_id)