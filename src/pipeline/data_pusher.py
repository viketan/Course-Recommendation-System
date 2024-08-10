import pymongo
import pandas as pd
import numpy as np
import sys
from src.constant import DATA_FILE_PATH,USERNAME,PASSWORD
from src.logger import logger
from src.exception import CustomException
np.random.seed(42)  # Set seed for reproducibility

def get_course_details():
    """
    Reads the course details from a CSV file, assigns unique course IDs, 
    and returns the DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing course details with course IDs.
    """
    try:
        logger.info("Reading Course details from csv")
        df = pd.read_csv(DATA_FILE_PATH)
        df['course_id'] = np.arange(1, len(df) + 1)  # Assign unique course IDs
        logger.info("Successfully read course details")
        return df
    except Exception as e:
        logger.exception(f"Error occured in getting course details:{e}")
        raise CustomException(e,sys)

def get_user_ratings():
    """
    Generates a DataFrame containing simulated user ratings for courses.

    Returns:
        pd.DataFrame: DataFrame with user IDs, course IDs, and ratings.
    """
    try:
        logger.info("Generating User Rating")
        num_users = 1000  # Number of unique users
        num_courses = 456  # Number of unique courses
        num_ratings = 10000  # Number of ratings to generate

        # Generate random user IDs, course IDs, and ratings
        user_ids = np.random.randint(1, num_users + 1, num_ratings)
        course_ids = np.random.randint(1, num_courses + 1, num_ratings)
        ratings = np.random.randint(1, 6, num_ratings)  # Ratings between 1 and 5

        # Create the DataFrame
        ratings_df = pd.DataFrame({
            'user_id': user_ids,
            'course_id': course_ids,
            'rating': ratings
        })

        # Remove duplicates: keep the first occurrence if duplicate exists
        ratings_df = ratings_df.drop_duplicates(subset=['user_id', 'course_id'])

        # Ensure the DataFrame has the required number of ratings
        while len(ratings_df) < num_ratings:
            # Generate additional ratings
            additional_user_ids = np.random.randint(1, num_users + 1, num_ratings - len(ratings_df))
            additional_course_ids = np.random.randint(1, num_courses + 1, num_ratings - len(ratings_df))
            additional_ratings = np.random.randint(1, 6, num_ratings - len(ratings_df))

            # Create additional DataFrame and append
            additional_df = pd.DataFrame({
                'user_id': additional_user_ids,
                'course_id': additional_course_ids,
                'rating': additional_ratings
            })

            # Concatenate and remove duplicates again
            ratings_df = pd.concat([ratings_df, additional_df]).drop_duplicates(subset=['user_id', 'course_id'])
        logger.info("Successfuly generated User rating")
        return ratings_df
    except Exception as e:
        logger.exception(f"Error in generating User Ratings: {e}")
        raise CustomException(e,sys)

def get_user_details():
    """
    Generates a DataFrame containing simulated user details including roles and goals.

    Returns:
        pd.DataFrame: DataFrame with user IDs, roles, and goals.
    """
    try: 
        logger.info("Generating user details")
        num_users = 1000  # Number of unique users

        # Define IT roles and goals
        roles = [
            'Data Scientist', 'Software Engineer', 'AI Specialist', 
            'Machine Learning Engineer', 'Data Analyst', 'DevOps Engineer', 
            'Cybersecurity Analyst', 'Database Administrator', 
            'Cloud Engineer', 'Business Intelligence Analyst'
        ]
        goals = [
            'Learn ML', 'Improve Python', 'Deepen AI knowledge', 
            'Master SQL', 'Enhance Data Visualization', 'Boost Cloud Skills', 
            'Strengthen Cybersecurity', 'Optimize Databases', 
            'Advance in DevOps', 'Explore BI Tools'
        ]

        # Generate random user data
        user_ids = np.arange(1, num_users + 1)
        user_roles = np.random.choice(roles, num_users)
        user_goals = np.random.choice(goals, num_users)

        # Create DataFrame
        users_df = pd.DataFrame({
            'user_id': user_ids,
            'role': user_roles,
            'goal': user_goals
        })
        logger.info("SuccessFully generated User details")
        return users_df
    except Exception as e:
        logger.exception(f"Exception occured in generating:{e}")
        raise CustomException(e,sys)

def push_to_mongodb(course_df, ratings_df, user_df):
    """
    Pushes the provided DataFrames to the MongoDB database.

    Args:
        course_df (pd.DataFrame): DataFrame containing course details.
        ratings_df (pd.DataFrame): DataFrame containing user ratings.
        user_df (pd.DataFrame): DataFrame containing user details.
    """
    try:
        logger.info(f"Initiating pushing data to MongoDB")
        database_name = "MOOC_DB"  # Name of the MongoDB database
        client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.oi8t9.mongodb.net/")
        db = client[database_name]  # Access the database

        # Mapping of collection names to DataFrames
        collections = {
            "Course_details": course_df,
            "Ratings": ratings_df,
            "User_details": user_df
        }

        # Insert each DataFrame into its corresponding MongoDB collection
        for collection_name, df in collections.items():
            collection = db[collection_name]
            collection.delete_many({})
            data_dict = df.to_dict("records")  # Convert DataFrame to list of dictionaries
            collection.insert_many(data_dict)  # Insert data into MongoDB collection
            logger.info(f"Data inserted successfully into {collection_name}!")
    except Exception as e:
        logger.exception(f"Error occured in pushing data to mongodb:{e}")
        raise CustomException(e,sys)

def data_pipeline():
    """
    Main function to generate data and push it to MongoDB.
    """
    try:
        course_df = get_course_details()  # Generate course details DataFrame
        ratings_df = get_user_ratings()  # Generate user ratings DataFrame
        user_df = get_user_details()  # Generate user details DataFrame
        push_to_mongodb(course_df, ratings_df, user_df)  # Push DataFrames to MongoDB
    except Exception as e:
        raise CustomException(e,sys)