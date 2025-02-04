import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
from tensorflow.keras.models import load_model

# Load data and models
def load_data():
    # Load content-based filtering data
    movies_dict = pickle.load(open('pickle_files/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('pickle_files/similarity.pkl', 'rb'))

    # # Load collaborative filtering data
    # user_id_map = pickle.load(open('pickle_files/user_id_map.pkl', 'rb'))
    # movie_id_map = pickle.load(open('pickle_files/movie_id_map.pkl', 'rb'))
    # movies_cf = pickle.load(open('pickle_files/movies.pkl', 'rb'))
    # model = load_model('pickle_files/deep_learning_model.keras')

    return movies, similarity

# Fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=46e56bc2f5117c4879f0871ad84806fe"
    data = requests.get(url)
    data = data.json()
    poster_path = data['posters'][0]['file_path'] if data['posters'] else None
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Content-based filtering recommendation
def content_based_recommend(movie, movies, similarity, n=5):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:n+1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# # Collaborative filtering recommendation
# def collaborative_filtering_recommend(user_id, movies_cf, model, user_id_map, movie_id_map, n=5):
#     user_index = user_id_map.get(user_id, None)
#     if user_index is None:
#         return [], []  # If user ID is not found, return empty lists
    
#     movie_indices = np.arange(len(movie_id_map))
#     user_indices = np.full(len(movie_id_map), user_index)

#     predictions = model.predict([user_indices, movie_indices]).flatten()
#     top_n_indices = predictions.argsort()[-n:][::-1]  # Get top N recommendations
#     top_movie_ids = [list(movie_id_map.keys())[i] for i in top_n_indices]  # Convert back to actual movie IDs
    
#     # Get movie titles and posters
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for movie_id in top_movie_ids:
#         movie_title = movies_cf[movies_cf['id'] == movie_id]['title'].values[0]
#         recommended_movie_names.append(movie_title)
#         recommended_movie_posters.append(fetch_poster(movie_id))
    
#     return recommended_movie_names, recommended_movie_posters

# Hybrid recommendation function
def hybrid_recommend(movie_title, movies, similarity, n=5):
    # Content-based recommendations
    cb_names, cb_posters = content_based_recommend(movie_title, movies, similarity, n)
    
    # # Collaborative filtering recommendations (if user_id is not provided, use a default user_id)
    # default_user_id = 1  # You can change this to any default user ID
    # cf_names, cf_posters = collaborative_filtering_recommend(default_user_id, movies_cf, model, user_id_map, movie_id_map, n)
    
    # Combine and deduplicate recommendations
    all_names = cb_names
    all_posters = cb_posters 
    unique_names, unique_posters = [], []
    seen = set()
    for name, poster in zip(all_names, all_posters):
        if name not in seen:
            seen.add(name)
            unique_names.append(name)
            unique_posters.append(poster)
    
    return unique_names[:n], unique_posters[:n]

# Streamlit app
def main():
    st.title("🎬 Movie Recommender System")
    st.markdown("""Welcome to the Movie Recommender System! Get personalized movie recommendations based on your preferences.""")

    # Load data and models
    movies, similarity = load_data()

    # Dropdown menu for genre selection
    if 'genres' in movies.columns:
        genre_list = movies['genres'].explode().unique()
    else:
        genre_list = []
    selected_genre = st.selectbox("Select a genre:", ["Select a genre"] + list(genre_list))

    # Dropdown menu for movie selection
    movie_list = movies['title'].unique()
    selected_movie = st.selectbox("Select a movie:", ["Select a movie"] + list(movie_list))

    # Button to trigger recommendations
    if st.button("Get Recommendations"):
        if selected_genre != "Select a genre":
            # Get a random movie from the selected genre
            genre_movies = movies[movies['genres'].apply(lambda x: selected_genre in x)]
            if not genre_movies.empty:
                selected_movie = genre_movies.iloc[0]['title']
                st.subheader(f"Top 5 Recommendations for '{selected_genre}' genre:")
            else:
                st.error("No movies found for the selected genre.")
        elif selected_movie != "Select a movie":
            st.subheader(f"Top 5 Recommendations based on '{selected_movie}':")
        else:
            st.error("Please select a genre or a movie.")

        # Get hybrid recommendations
        recommended_names, recommended_posters = hybrid_recommend(
            selected_movie, movies, similarity, n=5
        )

        # Initialize session state for pagination
        if 'start_index' not in st.session_state:
            st.session_state['start_index'] = 0

        # Function to display movie posters in a line with spacing
        def display_movie_posters(posters, names):
            cols = st.columns(len(posters))
            for col, poster, name in zip(cols, posters, names):
                col.image(poster, caption=name)

        # Display the posters
        display_movie_posters(recommended_posters, recommended_names)
if __name__ == "__main__":
    main()
