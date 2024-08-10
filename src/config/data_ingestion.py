from dataclasses import dataclass
import os
@dataclass
class DataIngestionArtififact():
    course_filepath: str = os.path.join('artifact','courses.csv')
    users_filepath: str = os.path.join('artifact','users.csv')
    ratings_filepath: str = os.path.join('artifact','ratings.csv')


