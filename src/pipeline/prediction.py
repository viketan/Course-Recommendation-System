from src.components.prediction import Prediction

class Predict:

    def initiate_prediction(self,user_id):
        predictor = Prediction()
        predictor.load_input_data()
        recommended_courses = predictor.hybrid_recommendations_with_context_and_content(user_id=user_id, top_n=10)
        return recommended_courses[['course_id', 'Title', 'Description', 'Instructor']]
