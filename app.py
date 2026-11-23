import streamlit as st
import pickle
import pandas as pd
import requests

# API KEY
API_KEY =[" http://www.omdbapi.com/?i=tt3896198&apikey=e60739ee"]

# Load data
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


# Recommendation function
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# Fetch movie poster
@st.cache_data
def fetch_poster(movie_name):

    url = "https://www.omdbapi.com/"

    params = {
        'apikey': API_KEY,
        't': movie_name
    }

    response = requests.get(url, params=params, timeout=10)

    data = response.json()

    if data.get('Response') == 'True':
        poster = data.get('Poster')

        if poster and poster != 'N/A':
            return poster

    return None


# Streamlit UI
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select your movie',
    movies['title'].values
)


if st.button('Recommend'):

    recommendations = recommend(selected_movie_name)

    st.subheader('Recommended Movies')

    cols = st.columns(5)

    for col, movie in zip(cols, recommendations):

        with col:

            poster = fetch_poster(movie)

            if poster:
                st.image(poster, use_container_width=True)

            else:
                st.write("Poster not available")

            st.caption(movie)