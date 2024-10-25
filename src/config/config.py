
import os

#------------------------------------------------------------------
# pip install python-dotenv
from dotenv import load_dotenv
mac_user = 'davidignacio'
env_path = f"/Users/{mac_user}/Documents/Python/tres60/Proyecto-Aceite/Others/worker-pipeline-weather/database.md"
load_dotenv(dotenv_path = env_path)
#------------------------------------------------------------------

# Environment variables
SERVICE="worker-pipeline-weather"

# API
API_BASE_URL: str = os.getenv("API_BASE_URL")
API_RETRIES: int = 3
API_TIMEOUT: int = 10
API_BACKOFF_FACTOR: int = 2

# PostgreSQL
POSTGRESQL_SERVER: str = os.getenv("POSTGRESQL_SERVER")
POSTGRESQL_DATABASE: str = os.getenv("POSTGRESQL_DATABASE")
POSTGRESQL_USER: str = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD: str = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_PORT: str = os.getenv("POSTGRESQL_PORT")