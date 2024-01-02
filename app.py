import pickle
import streamlit as st
import requests

movie = pickle.load(open('movie.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def movies_recommend(name):
    index = movie.loc[movie['title']==name,'title'].index
    movie_index = enumerate (similarity[index[0]])
    movies_recommended = sorted(movie_index, reverse=True, key=lambda x: x[1])[:5]
    index = [key for key,val in movies_recommended]
    index = movie.iloc[index,0]
    
    movies_recommended={}
    for ind in index:
        url = f"https://api.themoviedb.org/3/movie/{ind}?api_key=75eb0685f1f9140663e33eb0ea57150a&language=en-US"
        data=requests.get(url).json()
        movies_recommended[data['original_title']]=f"https://image.tmdb.org/t/p/w500/{data.get('poster_path')}"
    return movies_recommended

st.header('Movies Recommendation System')

movie_list = movie['title'].values
selected_movie = st.selectbox(
    "Input the name of a movie or choose one from the provided list",
    movie_list
)

if st.button('Display The Recommendations'):
    recommended_movie = movies_recommend(selected_movie)
    columns = st.columns(5)
    for col,title in zip(columns,recommended_movie.keys()):
        with col:
            st.image(recommended_movie[title])
            st.caption(title)

