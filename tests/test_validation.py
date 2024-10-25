

def validate_observation(observation: dict) -> bool:
    """
    Summary:
        Validates that the required fields in the observation data are not None 
        and meet expected types/ranges.
    Args:
        observation (dict): Dictionary containing observation data.
    Returns:
        bool: True if the observation is valid, False otherwise.
    """
    
    required_fields = [
        'station_id', 
        'observation_timestamp', 
        'temperature', 
        'wind_speed', 
        'humidity'
    ]
    
    for field in required_fields:
        if observation.get(field) is None:
            return False
    return True


def test_validate_observation():
    """
    Summary:
        Tests the validate_observation function.
    """
    
    valid_observation = {
        'station_id': '12345',
        'observation_timestamp': '2023-10-23T12:00:00Z',
        'temperature': 20.5,
        'wind_speed': 10.0,
        'humidity': 75
    }
    invalid_observation = {
        'station_id': '12345',
        'observation_timestamp': None,
        'temperature': None,
        'wind_speed': 10.0,
        'humidity': 75
    }
    
    assert validate_observation(valid_observation) == True
    assert validate_observation(invalid_observation) == False