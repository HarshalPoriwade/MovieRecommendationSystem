import streamlit as st
import pickle
import pandas as pd
import requests

OMDB_API_KEY = "39ece610"

def fetch_poster(movie_id):
    title = movies.loc[movies['movie_id'] == movie_id, 'title'].values
    if len(title) == 0:
        return "https://via.placeholder.com/300x450?text=No+Poster"
    title = title[0]
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={requests.utils.quote(title)}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster = data.get('Poster', '')
        if poster and poster != 'N/A':
            return poster
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster for '{title}': {e}")
        return "https://via.placeholder.com/300x450?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movie_list = pickle.load(open('movie_list.pkl','rb'))
movies = pd.DataFrame(movie_list)
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movie_list['title'].values

st.title('MOVIE RECOMMENDER SYSTEM')
option = st.selectbox(
    "Select a movie for recommendation", movie_list
)
if st.button("Recommend"):
    names, poster = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
