# Weather Data Pipeline

## Project Overview

This project is designed to build a weather data pipeline that extracts weather observations from the National Weather Service API, transforms the data, and loads it into a PostgreSQL database. The pipeline is designed to process data from the last 7 days on the first run and ensures only new records are inserted in subsequent runs. It also supports batch data insertion for improved performance and includes error handling.

## Features

- Extracts weather station data and observations from the [National Weather Service API](https://www.weather.gov/documentation/services-web-api).
- Handles data transformations, rounding numeric values to two decimal places and handling missing values.
- Loads weather data into a PostgreSQL database, ensuring no duplicate records.
- Supports batch inserts for efficient data handling.
- Includes error handling and logging for robust execution.
- Designed to insert only new records on subsequent runs.

## Requirements

- Python 3.11+
- PostgreSQL 12+
- Docker (for running PostgreSQL in a container)

* Servicio
* SERVICE
* Database
  * POSTGRESQL_SERVER
  * POSTGRESQL_USER
  * POSTGRESQL_PASSWORD
  * POSTGRESQL_DATABASE
  * POSTGRESQL_PORT
* Endpoints de Servicios
  * API_BASE_URL

## Environment Variables

To run the pipeline, the following environment variables are required:

**POSTGRESQL_SERVER**: The address of the PostgreSQL server.

**POSTGRESQL_USER**: Username for the PostgreSQL database.

**POSTGRESQL_PASSWORD**: Password for the PostgreSQL database.

**POSTGRESQL_DATABASE**: The name of the database to connect to.

**POSTGRESQL_PORT**: The port number for PostgreSQL (default is 5432).

**API_BASE_URL**: The base URL of the National Weather Service API.

## Execution

## PostgreSQL Execution

If you don’t have a PostgreSQL instance running, you can use Docker to spin up a containerized instance of PostgreSQL with the following command:

```bash
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
```

### Docker

1. Build Image
   docker build . -t worker-pipeline-weather
2. Iniciar el contenedor:
   docker run
   -ePOSTGRESQL_SERVER=server
   -ePOSTGRESQL_USER=user
   -ePOSTGRESQL_PASSWORD=password
   -ePOSTGRESQL_DATABASE=database
   -ePOSTGRESQL_PORT=port
   -eAPI_BASE_URL=api_url
   worker-pipeline-weather
3. Creatin main Table:
   docker exec -it weather-pipeline-container python create_table.py
4. Execute the Pipeline:
   docker exec -it weather-pipeline-container python pipeline.py
5. Query Data:
   docker exec -it weather-pipeline-container python extract_to_dataframe.py
6. Running Test:
   docker-compose run test

```bash
docker build . -t worker-pipeline-weather

docker run
-ePOSTGRESQL_SERVER=server
-ePOSTGRESQL_USER=user
-ePOSTGRESQL_PASSWORD=password
-ePOSTGRESQL_DATABASE=database
-ePOSTGRESQL_PORT=port
-eAPI_BASE_URL=api_url
worker-pipeline-weather

docker exec -it weather-pipeline-container python create_table.py

docker exec -it weather-pipeline-container python pipeline.py

docker exec -it weather-pipeline-container python extract_to_dataframe.py

docker-compose run test
```
