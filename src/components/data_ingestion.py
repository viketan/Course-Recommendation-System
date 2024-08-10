from src.config.data_ingestion import DataIngestionArtififact
from src.logger import logger
from src.exception import CustomException
from src.constant import USERNAME, PASSWORD, DB_NAME, COLLECTION_NAME
import pymongo
import pandas as pd
import sys,os

class DataIngestion:
    def __init__(self):
        """
        Initializes the DataIngestion class and sets up the DataIngestionArtifact instance.
        """
        self.artifact = DataIngestionArtififact()
        logger.info("DataIngestion class initialized with DataIngestionArtifact.")

    def connect_to_mongodb(self):
        """
        Establishes a connection to MongoDB and returns the database object.

        Returns:
            pymongo.database.Database: MongoDB database object.

        Raises:
            CustomException: If an error occurs while connecting to MongoDB.
        """
        try:
            logger.info("Connecting to MongoDB Server")
            client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.oi8t9.mongodb.net/")
            db = client[DB_NAME]
            logger.info("Successfully connected to MongoDB Server")
            return db
        except Exception as e:
            logger.exception("Error occurred while connecting to MongoDB Server")
            raise CustomException(e, sys)

    def fetch_data_from_mongodb(self, collection_name):
        """
        Fetches data from the specified MongoDB collection and loads it into a Pandas DataFrame.

        Args:
            collection_name (str): The name of the MongoDB collection to fetch data from.

        Returns:
            pd.DataFrame: DataFrame containing the fetched data.

        Raises:
            CustomException: If an error occurs while fetching data from MongoDB.
        """
        try:
            logger.info(f"Fetching data from collection: {collection_name}")
            db = self.connect_to_mongodb()
            collection = db[collection_name]
            data = list(collection.find())  # Fetch all data from the collection
            df = pd.DataFrame(data)  # Convert data to a Pandas DataFrame
            
            # Drop the MongoDB '_id' field if it exists, as it may not be needed
            if '_id' in df.columns:
                df = df.drop(columns=['_id'])
                
            logger.info(f"Successfully fetched data from collection: {collection_name}")
            return df
        except Exception as e:
            logger.exception(f"Error occurred while fetching data from collection: {collection_name}")
            raise CustomException(e, sys)

    def save_data_locally(self, df, file_name):
        """
        Saves the given DataFrame as a CSV file locally.

        Args:
            df (pd.DataFrame): DataFrame to be saved.
            file_name (str): The name of the file to save the data as.

        Raises:
            CustomException: If an error occurs while saving data to a CSV file.
        """
        try:
            # Create directory if it does not exist
            directory = os.path.dirname(file_name)
            if not os.path.exists(directory):
                logger.info(f"Creating directory: {directory}")
                os.makedirs(directory)
            logger.info(f"Saving DataFrame to CSV file: {file_name}")
            df.to_csv(file_name, index=False)  # Save DataFrame as a CSV file
            logger.info(f"Data saved to {file_name} successfully!")
        except Exception as e:
            logger.exception("Error occurred while saving data to CSV file")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        """
        Fetches data from MongoDB collections and saves them locally as CSV files.

        Uses the DataIngestionArtifact to determine the file paths for saving the data.
        """
        try:
            logger.info("Initiating data ingestion process.")
            
            # Fetch and save course details
            course_df = self.fetch_data_from_mongodb(COLLECTION_NAME[0])
            self.save_data_locally(course_df, self.artifact.course_filepath)
            
            # Fetch and save ratings
            ratings_df = self.fetch_data_from_mongodb(COLLECTION_NAME[1])
            self.save_data_locally(ratings_df, self.artifact.ratings_filepath)
            
            # Fetch and save user details
            user_df = self.fetch_data_from_mongodb(COLLECTION_NAME[2])
            self.save_data_locally(user_df, self.artifact.users_filepath)
            
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.exception("Error occurred during data ingestion")
            raise CustomException(e, sys)