import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'ml')

def load_data():
    print(f"Loading datasets from {DATA_DIR}...")
    
    movies_path = os.path.join(DATA_DIR, 'movies.csv')
    ratings_path = os.path.join(DATA_DIR, 'ratings.csv')
    tags_path = os.path.join(DATA_DIR, 'tags.csv')
    
    # Load movies
    movies = pd.read_csv(movies_path)
    
    # Load a sample of ratings (1M rows) to avoid MemoryError during initial EDA,
    # as the full dataset has 25M rows.
    print("Loading 1M ratings as a sample for EDA...")
    ratings = pd.read_csv(ratings_path, nrows=1000000) 
    
    # Load tags
    tags = pd.read_csv(tags_path)
    
    print("Data loading completed.\n")
    return movies, ratings, tags

def perform_basic_info(movies, ratings, tags):
    print("--- Movies DataFrame Info ---")
    print(movies.info())
    print("\nFirst 5 rows:")
    print(movies.head())
    print("-" * 40)
    
    print("\n--- Ratings DataFrame Info (Sample) ---")
    print(ratings.info())
    print("\nFirst 5 rows:")
    print(ratings.head())
    print("-" * 40)
    
    # Check for missing values
    print("\nMissing values in Movies:")
    print(movies.isnull().sum())
    
    print("\nMissing values in Ratings:")
    print(ratings.isnull().sum())
    print("-" * 40)

def plot_rating_distribution(ratings, output_dir):
    print("Generating Rating Distribution Plot...")
    plt.figure(figsize=(8, 6))
    sns.countplot(x='rating', data=ratings, palette='viridis')
    plt.title('Distribution of Movie Ratings (Sample of 1M)')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    
    output_path = os.path.join(output_dir, 'rating_distribution.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved to {output_path}")

def plot_top_genres(movies, output_dir):
    print("Generating Top Genres Plot...")
    # Movies can have multiple genres separated by '|'
    movies_copy = movies.copy()
    
    # Handle missing genres mostly labeled as '(no genres listed)'
    movies_copy['genres'] = movies_copy['genres'].replace('(no genres listed)', 'Unknown')
    movies_copy['genres'] = movies_copy['genres'].str.split('|')
    
    # Explode the genres so each genre gets its own row
    genres_exploded = movies_copy.explode('genres')
    
    plt.figure(figsize=(12, 8))
    genre_counts = genres_exploded['genres'].value_counts()
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='mako')
    
    plt.title('Most Common Movie Genres')
    plt.xlabel('Number of Movies')
    plt.ylabel('Genre')
    
    output_path = os.path.join(output_dir, 'top_genres.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved to {output_path}")
    
def plot_ratings_per_movie(ratings, movies, output_dir):
    print("Generating Most Rated Movies Plot...")
    # Count ratings per movie
    movie_rating_counts = ratings.groupby('movieId').size().reset_index(name='rating_count')
    # Merge with movie titles
    movie_rating_counts = movie_rating_counts.merge(movies[['movieId', 'title']], on='movieId')
    
    # Sort and take top 20
    top_movies = movie_rating_counts.sort_values(by='rating_count', ascending=False).head(20)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='rating_count', y='title', data=top_movies, palette='magma')
    plt.title('Top 20 Most Rated Movies (in the 1M Sample)')
    plt.xlabel('Number of Ratings')
    plt.ylabel('Movie Title')
    
    output_path = os.path.join(output_dir, 'most_rated_movies.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Saved to {output_path}")

def main():
    print("Starting Exploratory Data Analysis (EDA)...\n")
    
    # Create an output directory for plots if it doesn't exist
    plots_dir = os.path.join(BASE_DIR, 'eda_plots')
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        print(f"Created directory for plots: {plots_dir}")
    
    try:
        movies, ratings, tags = load_data()
        
        perform_basic_info(movies, ratings, tags)
        
        plot_rating_distribution(ratings, plots_dir)
        plot_top_genres(movies, plots_dir)
        plot_ratings_per_movie(ratings, movies, plots_dir)
        
        print("\nEDA finished successfully.")
    except FileNotFoundError as e:
        print(f"\nError: Could not find data files. Make sure they exist in the 'ml' directory. Details: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during EDA: {e}")

if __name__ == "__main__":
    main()
