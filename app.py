import streamlit as st
import pickle
import pandas as pd
import requests
import zipfile

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8cc1e8d4518999f04dad9e2ba1f35925&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load the movie data and similarity matrix
@st.cache(allow_output_mutation=True)
def load_data():
    # Extract similarity.pkl from ZIP file
    with zipfile.ZipFile('similarity.zip', 'r') as zip_ref:
        zip_ref.extractall('./similarity_folder')

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity.pkl
similarity_path = './similarity_folder/similarity.pkl'
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be connected?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i])





