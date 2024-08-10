from src.logger import logger
from src.exception import CustomException
from src.config.data_validation import DataValidationArtifact, DataValidationInput
import pandas as pd
import yaml
import sys

class DataValidation:
    def __init__(self):
        self.input = DataValidationInput()
        self.artifact = DataValidationArtifact()
    
    def validate_data(self, df):
        """
        Validate the data in the given DataFrame and write results to a YAML file.

        Args:
            df (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation results with pass/fail status and reasons for failure.
        """
        validation_results = {
            'missing_values': {},
            'data_types': {},
            'unique_constraints': {},
            'length_constraints': {},
            'status': 'Pass'  # Default to Pass, will be updated to Fail if any validation fails
        }

        try:
            # 1. Check for missing values in critical columns
            missing_values = df.isnull().sum()
            for column, count in missing_values[missing_values > 0].items():
                validation_results['missing_values'][column] = {
                    'status': 'Fail',
                    'reason': f'{count} missing values found'
                }
                validation_results['status'] = 'Fail'

            # 2. Check data types
            expected_dtypes = {
                'Title': 'object',
                'Instructor': 'object',
                'Keywords': 'object',
                'Learn': 'object',
                'Description': 'object',
                'course_id': 'int64'
            }
            for column, dtype in expected_dtypes.items():
                actual_dtype = str(df[column].dtype)
                if actual_dtype != dtype:
                    validation_results['data_types'][column] = {
                        'status': 'Fail',
                        'expected': dtype,
                        'actual': actual_dtype,
                        'reason': f'Expected {dtype} but got {actual_dtype}'
                    }
                    validation_results['status'] = 'Fail'
                else:
                    validation_results['data_types'][column] = {'status': 'Pass'}

            # 3. Validate unique constraints for 'course_id'
            if df['course_id'].duplicated().any():
                validation_results['unique_constraints']['course_id'] = {
                    'status': 'Fail',
                    'reason': 'Duplicate values found'
                }
                validation_results['status'] = 'Fail'
            else:
                validation_results['unique_constraints']['course_id'] = {'status': 'Pass'}

            # 4. Check length constraints (if applicable)
            length_constraints = {
                'Title': (1, 100),
                'Instructor': (1, 50),
                'Keywords': (1, 1000),
                'Learn': (1, 2000),
                'Description': (1, 2000)
            }
            for column, (min_length, max_length) in length_constraints.items():
                invalid_length = df[column].apply(lambda x: not (min_length <= len(str(x)) <= max_length))
                if invalid_length.any():
                    validation_results['length_constraints'][column] = {
                        'status': 'Fail',
                        'reason': f'Length constraints not met: should be between {min_length} and {max_length} characters'
                    }
                    validation_results['status'] = 'Fail'
                else:
                    validation_results['length_constraints'][column] = {'status': 'Pass'}

            return validation_results
        except Exception as e:
            logger.exception(f"Error occurred in Data Validation: {e}")
            raise CustomException(e, sys)

    def initiate_data_validation(self):
        try:
            df = pd.read_csv(self.input.course_filepath)
            results = self.validate_data(df)
            # Write results to YAML file
            with open(self.artifact.report_filepath, 'w') as file:
                yaml.dump(results, file, default_flow_style=False)
            logger.info(f"Data validation report written to {self.artifact.report_filepath}")
        except Exception as e:
            logger.exception(f"Error occurred in data validation: {e}")
            raise CustomException(e, sys)
