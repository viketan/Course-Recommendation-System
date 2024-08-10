import streamlit as st
from src.pipeline.prediction import Predict
import pandas as pd

# Initialize the Prediction class
predictor = Predict()
USERS_PATH = 'artifact/users.csv'

def load_users():
    try:
        users = pd.read_csv(USERS_PATH)
        return users
    except Exception as e:
        st.error(f"Failed to load user data: {e}")
        return None

def get_recommendations(user_id, top_n=10):
    recommended_courses= predictor.initiate_prediction(user_id)
    return recommended_courses

def main():
    st.title('Course Recommendation System')

    st.sidebar.header('Input')
    user_id = st.sidebar.number_input('Enter User ID:', min_value=1, step=1)
    

    if st.sidebar.button('Get Recommendations'):
        st.write(f"Fetching recommendations for User ID: {user_id}")

        try:
            # Get recommendations
            if 1 <= user_id <= 999:
                recommendations = get_recommendations(user_id)
                users = load_users()
                user_details = users[users['user_id']==user_id]
                st.write(user_details[['user_id', 'role', 'goal']])
                st.write("### Recommended Courses:")
                st.dataframe(recommendations[['course_id', 'Title', 'Description', 'Instructor']])
            else:
                st.error("User Not Registered")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
