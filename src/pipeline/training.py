from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.logger import logger
from src.exception import CustomException
import sys

class Train:
    def initiate_training(self):
        """
        Orchestrates the end-to-end training process, including data ingestion, validation, and transformation.
        """
        try:
            # Data Ingestion
            logger.info("Starting data ingestion process.")
            ingestor = DataIngestion()
            ingestor.initiate_data_ingestion()
            logger.info("Data ingestion completed successfully.")

            # Data Validation
            logger.info("Starting data validation process.")
            validator = DataValidation()
            validator.initiate_data_validation()
            logger.info("Data validation completed successfully.")

            # Data Transformation
            logger.info("Starting data transformation process.")
            transformer = DataTransformation()
            transformer.initiate_data_transformation()
            logger.info("Data transformation completed successfully.")

        except CustomException as ce:
            logger.error(f"Custom exception occurred during training: {ce}")
            raise ce

        except Exception as e:
            logger.error(f"An unexpected error occurred during training: {e}")
            raise CustomException(e, sys)

        logger.info("Training process completed successfully.")

