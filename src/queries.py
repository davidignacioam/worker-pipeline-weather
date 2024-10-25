
# Project
from config.database import get_db_connection


def get_average_temperature_last_week():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT AVG(temperature)
            FROM weather_data
            WHERE observation_timestamp >= NOW() - INTERVAL '7 days';
        ''')
        avg_temp = cursor.fetchone()[0]
    conn.close()
    return avg_temp


def get_max_wind_speed_change():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            WITH wind_diff AS (
                SELECT observation_timestamp, wind_speed,
                LAG(wind_speed) OVER (ORDER BY observation_timestamp) AS prev_wind_speed
                FROM weather_data
                WHERE observation_timestamp >= NOW() - INTERVAL '7 days'
            )
            SELECT MAX(ABS(wind_speed - prev_wind_speed)) AS max_wind_speed_change
            FROM wind_diff
            WHERE prev_wind_speed IS NOT NULL;
        ''')
        max_wind_change = cursor.fetchone()[0]
    conn.close()
    return max_wind_change


# Get the average temperature
average_temp = get_average_temperature_last_week()
print(f"Average Temperature in the last week: {average_temp}")

# Get the max wind speed change
max_wind_speed_change = get_max_wind_speed_change()
print(f"Maximum Wind Speed Change in the last week: {max_wind_speed_change}")