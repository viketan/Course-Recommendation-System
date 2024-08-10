from dotenv import load_dotenv
import os
import urllib
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
USERNAME = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
PASSWORD = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
DB_NAME = os.getenv("MONGO_DB_NAME") # URL-encoded password for MongoDB
DATA_FILE_PATH = 'Data/courses.csv'
TIMESTAMP = datetime.now().strftime("%Y%m%d:%H%M%S")
COLLECTION_NAME  = [
            "Course_details",
            "Ratings",
            "User_details"
        ]