"""
Phase 2: Data Preprocessing & TMDb Enrichment
----------------------------------------------
Cleans MovieLens 25M data, enriches movies via the TMDb API (with caching),
and prepares a combined_features column for content-based filtering.

Outputs:
  ml/movies_enriched.csv  — movies + TMDb metadata + combined features
  ml/ratings_clean.csv    — deduplicated ratings
  ml/tmdb_cache.json      — cached TMDb API responses
"""

import os
import re
import json
import time
import requests
import pandas as pd
from apikey import Api_key

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "ml")

TMDB_API_KEY = Api_key
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_RATE_LIMIT = 0.03  # ~33 req/s (TMDb allows ~40/s, keep a margin)

CACHE_PATH = os.path.join(DATA_DIR, "tmdb_cache.json")

# ─── Helpers ──────────────────────────────────────────────────────────────────

def extract_year_and_title(title: str):
    """
    Extracts the year and clean title from strings like 'Toy Story (1995)'.
    Returns (clean_title, year).  Year is None if not found.
    """
    match = re.search(r"\((\d{4})\)\s*$", title)
    if match:
        year = int(match.group(1))
        clean_title = title[: match.start()].strip()
        return clean_title, year
    return title.strip(), None


def load_tmdb_cache() -> dict:
    """Load cached TMDb results from disk."""
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_tmdb_cache(cache: dict):
    """Persist TMDb cache to disk."""
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


def query_tmdb(title: str, year, cache: dict) -> dict:
    """
    Query TMDb for a movie.  Returns dict with overview, poster_path,
    vote_average, popularity.  Uses cache to avoid duplicate calls.
    """
    cache_key = f"{title}_{year}"
    if cache_key in cache:
        return cache[cache_key]

    params = {"api_key": TMDB_API_KEY, "query": title}
    if year is not None:
        params["year"] = int(year)

    empty_result = {
        "overview": "",
        "poster_path": "",
        "vote_average": 0.0,
        "popularity": 0.0,
    }

    try:
        resp = requests.get(TMDB_SEARCH_URL, params=params, timeout=10)
        if resp.status_code == 429:
            # Rate limited — wait and retry once
            time.sleep(2)
            resp = requests.get(TMDB_SEARCH_URL, params=params, timeout=10)

        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                top = results[0]
                result = {
                    "overview": top.get("overview", ""),
                    "poster_path": top.get("poster_path", ""),
                    "vote_average": top.get("vote_average", 0.0),
                    "popularity": top.get("popularity", 0.0),
                }
                cache[cache_key] = result
                return result

        cache[cache_key] = empty_result
        return empty_result

    except requests.RequestException:
        cache[cache_key] = empty_result
        return empty_result


# ─── Stage 1: Data Cleaning ──────────────────────────────────────────────────

def clean_data():
    """Load and clean movies, ratings, and tags."""
    print("=" * 60)
    print("STAGE 1 — DATA CLEANING")
    print("=" * 60)

    # --- Movies ---
    movies = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))
    print(f"Loaded {len(movies)} movies.")

    # Extract year and clean title
    movies[["clean_title", "year"]] = movies["title"].apply(
        lambda t: pd.Series(extract_year_and_title(t))
    )
    movies["year"] = movies["year"].astype("Int64")  # nullable int

    # Normalize genres
    movies["genres"] = movies["genres"].replace("(no genres listed)", "Unknown")
    print(f"  Year range: {movies['year'].min()} – {movies['year'].max()}")
    print(f"  Movies with unknown genre: {(movies['genres'] == 'Unknown').sum()}")

    # --- Ratings ---
    print("\nLoading ratings (full dataset — this may take a moment)...")
    ratings = pd.read_csv(os.path.join(DATA_DIR, "ratings.csv"))
    before = len(ratings)
    ratings.drop_duplicates(subset=["userId", "movieId"], keep="last", inplace=True)
    after = len(ratings)
    print(f"  Loaded {before} ratings, removed {before - after} duplicates → {after} remain.")

    # --- Tags ---
    tags = pd.read_csv(os.path.join(DATA_DIR, "tags.csv"))
    tags["tag"] = tags["tag"].astype(str).str.lower().str.strip()
    print(f"  Loaded {len(tags)} tags.")

    return movies, ratings, tags


# ─── Stage 2: TMDb Enrichment ────────────────────────────────────────────────

def enrich_with_tmdb(movies: pd.DataFrame):
    """Query TMDb for overview, poster, vote_average, popularity."""
    print("\n" + "=" * 60)
    print("STAGE 2 — TMDb ENRICHMENT")
    print("=" * 60)

    cache = load_tmdb_cache()
    already_cached = sum(
        1 for _, row in movies.iterrows()
        if f"{row['clean_title']}_{row['year']}" in cache
    )
    to_fetch = len(movies) - already_cached
    print(f"  Cache has {already_cached} entries. Need to fetch {to_fetch} from TMDb.")

    if to_fetch == 0:
        print("  All movies already cached — skipping API calls.")
    else:
        est_minutes = round(to_fetch * TMDB_RATE_LIMIT / 60, 1)
        print(f"  Estimated time: ~{est_minutes} minutes")

    overviews, posters, votes, pops = [], [], [], []
    save_interval = 500  # save cache every N movies

    for idx, row in movies.iterrows():
        result = query_tmdb(row["clean_title"], row["year"], cache)
        overviews.append(result["overview"])
        posters.append(result["poster_path"])
        votes.append(result["vote_average"])
        pops.append(result["popularity"])

        time.sleep(TMDB_RATE_LIMIT)

        # Progress & cache checkpoint
        count = idx + 1
        if count % save_interval == 0:
            save_tmdb_cache(cache)
            print(f"    … processed {count}/{len(movies)} movies (cache saved)")

    movies["overview"] = overviews
    movies["poster_path"] = posters
    movies["tmdb_vote_average"] = votes
    movies["tmdb_popularity"] = pops

    save_tmdb_cache(cache)
    print(f"  TMDb enrichment complete. Cache saved ({len(cache)} entries).")

    return movies


# ─── Stage 3: Feature Preparation ────────────────────────────────────────────

def prepare_features(movies: pd.DataFrame, tags: pd.DataFrame):
    """Build the combined_features column for content-based filtering."""
    print("\n" + "=" * 60)
    print("STAGE 3 — FEATURE PREPARATION")
    print("=" * 60)

    # Aggregate tags per movie
    tags_agg = (
        tags.groupby("movieId")["tag"]
        .apply(lambda x: " ".join(x))
        .reset_index()
        .rename(columns={"tag": "tags_combined"})
    )
    movies = movies.merge(tags_agg, on="movieId", how="left")
    movies["tags_combined"] = movies["tags_combined"].fillna("")

    # Build combined features: genres + overview + tags
    movies["combined_features"] = (
        movies["genres"].str.replace("|", " ", regex=False)
        + " " + movies["overview"].fillna("")
        + " " + movies["tags_combined"]
    ).str.strip()

    print(f"  combined_features sample (movieId=1):")
    sample = movies.loc[movies["movieId"] == 1, "combined_features"].values
    if len(sample):
        print(f"    {sample[0][:200]}...")

    return movies


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    start = time.time()

    movies, ratings, tags = clean_data()
    movies = enrich_with_tmdb(movies)
    movies = prepare_features(movies, tags)

    # Save outputs
    enriched_path = os.path.join(DATA_DIR, "movies_enriched.csv")
    ratings_path = os.path.join(DATA_DIR, "ratings_clean.csv")

    movies.to_csv(enriched_path, index=False)
    ratings.to_csv(ratings_path, index=False)

    elapsed = round(time.time() - start, 1)
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"  Saved: {enriched_path}")
    print(f"  Saved: {ratings_path}")
    print(f"  Total columns in enriched: {list(movies.columns)}")
    print(f"  Total time: {elapsed}s")


if __name__ == "__main__":
    main()
