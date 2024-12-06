import pickle
import streamlit as st
import requests
import time  # For loading spinner

# Fetch movie poster and description from TMDb API
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    overview = data.get('overview', 'Description not available.')
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
    return full_path, overview

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, description = fetch_movie_details(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_descriptions.append(description)
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions

# Streamlit app layout
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# App styles and animations
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #141E30, #243B55);
        color: white;
    }
    .header {
        background-color: #4CAF50;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .movie-card:hover {
        transform: scale(1.05);
        transition: 0.3s ease-in-out;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: lightgray;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with animation
st.markdown(
    '<div class="header">🎥 Movie Recommender System 🎥</div>',
    unsafe_allow_html=True,
)

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown menu for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🔍 Type or select a movie from the dropdown",
    movie_list,
    help="Start typing a movie name or select one from the list."
)

# Show recommendations with a spinner
if st.button('🎬 Show Recommendations'):
    with st.spinner('Fetching recommendations...'):
        time.sleep(2)  # Simulate loading time
        recommended_movie_names, recommended_movie_posters, recommended_movie_descriptions = recommend(selected_movie)

    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>Recommended Movies</h3>", unsafe_allow_html=True)

    # Responsive grid layout for movies with descriptions
    for i in range(len(recommended_movie_names)):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(recommended_movie_posters[i], use_container_width='always', caption=recommended_movie_names[i])
        with col2:
            st.markdown(f"**{recommended_movie_names[i]}**")
            st.write(recommended_movie_descriptions[i])

# Add footer with icons
st.markdown(
    """
    <div class="footer">
        Made with ❤️ by <a href="https://github.com/your-profile" target="_blank">Jagrat Gupta</a> | 
        <a href="https://www.linkedin.com/in/your-profile/" target="_blank">LinkedIn</a> | 
        <a href="https://twitter.com/your-profile" target="_blank">Twitter</a>
    </div>
    """,
    unsafe_allow_html=True,
)
