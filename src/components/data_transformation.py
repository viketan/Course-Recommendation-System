from src.logger import logger
from src.exception import CustomException
from src.config.data_transformation import DataTransformationArtifact, DataTransformationInput
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import joblib
from scipy.sparse import save_npz

class DataTransformation:
    def __init__(self):
        self.input = DataTransformationInput()
        self.artifact = DataTransformationArtifact()

    def get_vectors(self, df):
        """
        Combines relevant text fields and generates a TF-IDF vector matrix.

        Args:
            df (pd.DataFrame): The DataFrame containing the course data.

        Returns:
            np.ndarray: TF-IDF matrix as a NumPy array.
        """
        try:
            logger.info("Combining text fields for TF-IDF vectorization.")
            df['combined_text'] = df['Title'] + " " + df['Description'] + " " + df['Instructor'] + " " + df['Learn'] + " " + df['Keywords']

            logger.info("Vectorizing text data using TF-IDF.")
            tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=5000)
            tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_text'])

            logger.info("TF-IDF vectorization completed successfully.")
            return tfidf_vectorizer,tfidf_matrix
        except Exception as e:
            logger.exception(f"Error occurred during TF-IDF vectorization: {e}")
            raise CustomException(e, sys)

    def get_cleaned_data(self, df):
        """
        Cleans the DataFrame by filling missing values in specific columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the course data.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        try:
            logger.info("Cleaning data by filling missing values in 'Instructor', 'Keywords', and 'Learn' columns.")
            df['Instructor'] = df['Instructor'].fillna(' ')
            df['Keywords'] = df['Keywords'].fillna(' ')
            df['Learn'] = df['Learn'].fillna(' ')
            logger.info("Data cleaning completed successfully.")
            return df
        except Exception as e:
            logger.exception(f"Error occurred during data cleaning: {e}")
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        """
        Orchestrates the data transformation process, including cleaning data,
        vectorizing text, and saving the resulting NumPy array to a CSV file.
        """
        try:
            logger.info("Initiating data transformation process.")
            
            # Load the data
            df = pd.read_csv(self.input.course_filepath)
            logger.info(f"Data loaded successfully from {self.input.course_filepath}.")
            
            # Clean the data
            df = self.get_cleaned_data(df)
            
            # Generate TF-IDF vectors
            tfidf_vectorizer, matrix = self.get_vectors(df)
            
            # Save the NumPy array to a CSV file
            save_npz(self.artifact.vector_filepath, matrix)
            logger.info(f"Array saved to {self.artifact.vector_filepath} successfully!")

            # Save the TfidfVectorizer object for later use
            joblib.dump(tfidf_vectorizer, self.artifact.vectorizer_filepath)
            logger.info(f"Vectorizer saved to {self.artifact.vectorizer_filepath} successfully!")
        
        
        except Exception as e:
            logger.exception(f"Error occurred during data transformation: {e}")
            raise CustomException(e, sys)
