
# External
from unittest.mock import patch

# Project
from pipeline.extract import get_station_data, get_observations


@patch('pipeline.extract.requests.get')
def test_get_station_data(mock_get):
    mock_get.return_value.json.return_value = {
        'id': '12345', 
        'name': 'Test Station'
    }
    mock_get.return_value.status_code = 200
    
    station_data = get_station_data('12345')
    assert station_data['id'] == '12345'
    assert station_data['name'] == 'Test Station'


@patch('pipeline.extract.requests.get')
def test_get_observations(mock_get):
    mock_get.return_value.json.return_value = {
        'features': [{'properties': {'temperature': {'value': 20.5}}}]
    }
    mock_get.return_value.status_code = 200
    
    observations = get_observations('12345')
    assert len(observations) > 0
    assert 'temperature' in observations[0]['properties']