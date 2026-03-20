
import streamlit as st
import pandas as pd
import pickle
import requests
import os
import gdown 

st.title('Movie Recommendation System')

# Download large files from Google Drive if not present


if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/file/d/1OBs-6uB-wyW-rHogZQDIVViEDVGHpCwb/view?usp=drive_link", "similarity.pkl", quiet=False)

mov = pickle.load(open('movve.pkl', 'rb'))
sim = pickle.load(open('similarity.pkl', 'rb'))

TMDB_API_KEY = st.secrets["keys"]

def fetch_poster(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(flim):
    movie_index = mov[mov['title'] == flim].index[0]
    distances = sim[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = [flim]
    for i in movies_list:
        recommended_movies.append(mov.iloc[i[0]].title)
    
    return recommended_movies

option = st.selectbox('Movies list', mov['title'].values)

if st.button('Search'):
    recommendations = recommend(option)

    posters = [fetch_poster(title) for title in recommendations]
    
    cols = st.columns(len(recommendations))
    for col, title, poster in zip(cols, recommendations, posters):
        with col:
            st.image(poster, width=150) 
            st.caption(title)
