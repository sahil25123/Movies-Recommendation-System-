import numpy as np
import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv('movies.csv')
credits = pd.read_csv('credits.csv')

# Merge movies and credits datasets on title
movies = movies.merge(credits, on='title')

# Keep only necessary columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Drop rows with missing values
movies.dropna(inplace=True)

# Function to convert JSON-like strings to a list of names
def convert(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except (ValueError, SyntaxError):
        return []

# Apply conversion functions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Function to extract top 3 cast members
def convert3(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)[:3]]
    except (ValueError, SyntaxError):
        return []

movies['cast'] = movies['cast'].apply(convert3)

# Function to extract director names
def fetch_director(text):
    try:
        return [i['name'] for i in ast.literal_eval(text) if i['job'] == 'Director']
    except (ValueError, SyntaxError):
        return []

movies['crew'] = movies['crew'].apply(fetch_director)

# Function to remove spaces in names
def collapse(L):
    return [i.replace(" ", "") for i in L]

# Apply collapse to clean up data
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

# Split overview into words and combine all features into a 'tags' column
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Create a new dataframe with movie ID, title, and tags
new = movies[['movie_id', 'title', 'tags']].copy()
new['tags'] = new['tags'].apply(lambda x: " ".join(x))

# Convert tags into vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()

# Compute cosine similarity
similarity = cosine_similarity(vector)

# Recommendation function
def recommend(movie):
    movie = movie.lower()
    if movie not in new['title'].str.lower().values:
        print(f"Movie '{movie}' not found in the dataset.")
        return
    
    index = new[new['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    print(f"Movies similar to '{movie.title()}':")
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)

# Example recommendation
recommend('Gandhi')

# Save models using pickle
pickle.dump(new, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
