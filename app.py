import streamlit as st
import pickle
import joblib
import pandas as pd
import requests
from PIL import Image
from io import BytesIO


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_description(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    description = data.get('overview', 'Description not available.')
    return description

def resize_image(image_url, height):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    width_percent = (height / float(img.size[1]))
    width = int((float(img.size[0]) * float(width_percent)))
    img = img.resize((width, height), Image.LANCZOS)
    return img


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_desc = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        movie_desc = fetch_description(movie_id)
        recommended_desc.append(movie_desc)
        # fetch poster from API
        # recommended_movies_posters.append(fetch_poster(movie_id))
        poster_url = fetch_poster(movie_id)
        recommended_movies_posters.append(resize_image(poster_url, 300))

    return recommended_movies, recommended_desc, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select The Movie Title', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_desc, recommended_movie_posters = recommend(selected_movie_name)
    
    for i in range(len(recommended_movie_names)):
        # Create a row with two columns: one for the name and tagline, and one for the poster
        row = st.columns([2, 1])  # Adjust the ratios as needed
        with row[0]:
            # st.text(recommended_movie_names[i])
            st.markdown(f"**<h3>{recommended_movie_names[i]}</h3>**", unsafe_allow_html=True)
            st.markdown(recommended_movie_desc[i])  # Show tagline underneath the movie name
        with row[1]:
            st.image(recommended_movie_posters[i])  # Display resized image

        st.markdown("------------------------------------------------")

# if st.button('Show Recommendation'):
#     recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])

#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])
