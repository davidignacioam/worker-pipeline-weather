
# External
from datetime import datetime

# Project
from pipeline.transform import transform_observation


def test_transform_observation():
    raw_observation = {
        'properties': {
            'timestamp': '2023-10-23T12:00:00Z',
            'temperature': {'value': 20.567},
            'windSpeed': {'value': 10.456},
            'relativeHumidity': {'value': 75.123}
        }
    }
    
    transformed = transform_observation(raw_observation)
    
    assert transformed['observation_timestamp'] == datetime(2023, 10, 23, 12, 0)
    assert transformed['temperature'] == 20.57 
    assert transformed['wind_speed'] == 10.46 
    assert transformed['humidity'] == 75.12 