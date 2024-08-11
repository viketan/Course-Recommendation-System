from src.logger import logger
from src.exception import CustomException
from src.config.prediction import PredictionInput
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import sys
import numpy as np
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

class Prediction:
    def __init__(self):
        self.input = PredictionInput()

    def load_input_data(self):
        try:
            self.courses = pd.read_csv(self.input.course_filepath)
            self.users = pd.read_csv(self.input.users_filepath)
            self.ratings = pd.read_csv(self.input.ratings_filepath)
            self.vectorizer = joblib.load(self.input.vectorizer_filepath)
            self.vectors = pd.read_csv(self.input.tf_idf_filepath)
            logger.info("Data and vectorizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading input data: {e}")
            raise CustomException(e, sys)

    def match_courses_with_context(self, user_id, top_n=3):
        try:
            user_context_str = self.users.loc[user_id, 'role'] + " " + self.users.loc[user_id, 'goal']
            user_context_vector = self.vectorizer.transform([user_context_str])
            cosine_similarities = cosine_similarity(user_context_vector, self.vectors).flatten()
            top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]
            context_recommendations = self.courses.iloc[top_n_indices]
            return context_recommendations['course_id'].tolist()
        except Exception as e:
            logger.error(f"Error in context-based recommendation for user {user_id}: {e}")
            raise CustomException(e, sys)

    def content_based_recommendations(self, user_id, top_n=3):
        try:
            # Get the courses the user has already rated
            user_ratings = self.ratings[self.ratings['user_id'] == user_id]
            rated_courses = user_ratings['course_id'].tolist()

            # Vectorize the descriptions of these courses
            user_profile_vector = self.vectors[self.courses['course_id'].isin(rated_courses)].mean(axis=0)

            # Compute cosine similarities between the user profile vector and all course vectors
            cosine_similarities = cosine_similarity([user_profile_vector], self.vectors).flatten()
            top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]
            content_recommendations = self.courses.iloc[top_n_indices]
            return content_recommendations['course_id'].tolist()
        except Exception as e:
            logger.error(f"Error in content-based recommendation for user {user_id}: {e}")
            raise CustomException(e, sys)

    def svd_recommendations(self, user_id, top_n=3):
        try:
            user_item_matrix = self.ratings.pivot(index='user_id', columns='course_id', values='rating').fillna(0)
            user_item_matrix_sparse = csr_matrix(user_item_matrix.values)
            U, sigma, Vt = svds(user_item_matrix_sparse, k=20)
            sigma = np.diag(sigma)
            user_factors = np.dot(np.dot(U, sigma), Vt)
            user_ratings = user_factors[user_id - 1]
            recommended_items = pd.Series(user_ratings, index=user_item_matrix.columns).sort_values(ascending=False)
            recommended_courses = recommended_items.index[recommended_items > 0].tolist()
            return recommended_courses[:top_n]
        except Exception as e:
            logger.error(f"Error in SVD recommendation for user {user_id}: {e}")
            raise CustomException(e, sys)

    def hybrid_recommendations_with_context_and_content(self, user_id, top_n=3, weights=None):
        try:
            if weights is None:
                weights = {
                    'svd': 0.4,
                    'context': 0.3,
                    'content': 0.3
                }
            svd_recs = self.svd_recommendations(user_id, top_n)
            context_recs = self.match_courses_with_context(user_id, top_n)
            content_recs = self.content_based_recommendations(user_id, top_n)

            course_scores = {}

            def update_scores(recommendations, weight):
                for course in recommendations:
                    if course in course_scores:
                        course_scores[course] += weight
                    else:
                        course_scores[course] = weight

            update_scores(svd_recs, weights.get('svd', 1.0))
            update_scores(context_recs, weights.get('context', 1.0))
            update_scores(content_recs, weights.get('content', 1.0))

            sorted_courses = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)
            top_course_ids = [course_id for course_id, score in sorted_courses[:top_n]]
            recommended_courses = self.courses[self.courses['course_id'].isin(top_course_ids)]

            logger.info(f"Hybrid recommendations generated for user {user_id}.")
            return recommended_courses
        except Exception as e:
            logger.error(f"Error in hybrid recommendation system for user {user_id}: {e}")
            raise CustomException(e, sys)
