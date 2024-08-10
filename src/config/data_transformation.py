from dataclasses import dataclass
import os
@dataclass
class DataTransformationInput():
    course_filepath: str = os.path.join('artifact','courses.csv')

class DataTransformationArtifact():
    vector_filepath: str =  os.path.join('artifact','tf-idf.csv')
    vectorizer_filepath: str = os.path.join('artifact','vectorizer.pkl')