from dataclasses import dataclass
import os
@dataclass
class DataValidationInput():
    course_filepath: str = os.path.join('artifact','courses.csv')

class DataValidationArtifact():
    report_filepath: str =  os.path.join('artifact','report.yaml')