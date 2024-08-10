import argparse
from src.pipeline.data_pusher import data_pipeline
from src.pipeline.training import Train
from src.pipeline.prediction import Predict
from src.logger import logger
from src.exception import CustomException
import sys

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Data Ingestion and Training Pipeline")

    # Add arguments for data pipeline
    parser.add_argument(
        '--run-data-pipeline', 
        action='store_true', 
        help="Flag to run the data pipeline"
    )

    # Add arguments for training pipeline
    parser.add_argument(
        '--run-training', 
        action='store_true', 
        help="Flag to run the training pipeline"
    )
    
    # Add arguments for prediction pipeline
    parser.add_argument(
        '--run-prediction', 
        action='store_true', 
        help="Flag to run the prediction pipeline"
    )
    
    # Add argument for user_id in prediction
    parser.add_argument(
        '--user-id', 
        type=int, 
        help="User ID for generating predictions", 
        required='--run-prediction' in sys.argv  # Make this argument required if --run-prediction is used
    )
    
    # Parse the arguments
    args = parser.parse_args()

    try:
        if args.run_data_pipeline:
            logger.info("Initiating data pipeline")
            data_pipeline()
            logger.info("Successfully completed data pipeline")

        if args.run_training:
            logger.info("Initiating training pipeline")
            trainer = Train()
            trainer.initiate_training()
            logger.info("Successfully completed training pipeline")
        
        if args.run_prediction:
            if args.user_id is None:
                raise ValueError("User ID must be provided for the prediction pipeline")
                
            logger.info("Initiating prediction pipeline")
            pred = Predict()
            print(pred.initiate_prediction(args.user_id))
            logger.info("Successfully completed prediction pipeline")

    except Exception as e:
        logger.exception("An error occurred during pipeline execution")
        raise CustomException(e, sys)

if __name__ == "__main__":
    main()
