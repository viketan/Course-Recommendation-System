from dataclasses import dataclass
import os
@dataclass
class PredictionInput():
    course_filepath: str = os.path.join('artifact','courses.csv')
    users_filepath: str = os.path.join('artifact','users.csv')
    ratings_filepath: str = os.path.join('artifact','ratings.csv')
    tf_idf_filepath: str = os.path.join('artifact','tf-idf.csv')
    vectorizer_filepath: str = os.path.join('artifact','vectorizer.pkl')

