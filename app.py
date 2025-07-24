import streamlit as st
import pickle
import requests
st.title("Movie Recommender System 📽️")

def fetch_poster(movie_id):
    TMDB_API_KEY = st.secrets["tmdb"]["api_key"]
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://tse3.mm.bing.net/th/id/OIP.IMYEa-ECkbVQ66EO1LCUDwHaHa?rs=1&pid=ImgDetMain&o=7&rm=3"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movie_list = pickle.load(open('movies.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movie_list['title'].values
option = st.selectbox(
    "Search Movie Name here.....",
    movie_list,
)

if st.button("Recommend"):
    names, poster = recommend(option)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if poster[i]:  # Show image only if valid
                st.image(poster[i])
            else:
                st.image("https://tse3.mm.bing.net/th/id/OIP.IMYEa-ECkbVQ66EO1LCUDwHaHa?rs=1&pid=ImgDetMain&o=7&rm=3")


st.markdown(
    """
    <hr style="margin-top: 2em;">
    <div style='text-align: center;'>
        Made with ❤️ by Vedant Kawade  
        <br>
        <a href='www.linkedin.com/in/vedantkawade3' target='_blank'>
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" alt="LinkedIn" width="30" height="30">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)