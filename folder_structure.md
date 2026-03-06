# Folder Structure

This document outlines the planned directory structure for the Movie Recommendation System.

```text
movie-recommendation/
├── .gsd/                   # GSD state, specs, and roadmap files
├── .agent/                 # Agent configuration and workflows
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints and routers
│   │   ├── core/           # Configuration, security, and setups
│   │   ├── models/         # Data models (Pydantic, database)
│   │   ├── services/       # Recommendation logic, TMDb integration
│   │   └── main.py         # FastAPI entry point
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Streamlit application
│   ├── pages/              # Streamlit multi-pages (e.g., search, recommendations)
│   ├── components/         # Reusable UI components
│   ├── assets/             # Images, styles, static assets
│   ├── app.py              # Streamlit entry point
│   └── requirements.txt    # Frontend dependencies
├── ml/                     # Machine Learning Database and Context
│   ├── README.txt          # ML datasets info
│   ├── movies.csv          # Movie dataset
│   ├── ratings.csv         # User ratings dataset
│   ├── tags.csv            # User tags for movies
│   ├── links.csv           # IMDB/TMDB links
│   ├── genome-scores.csv   # Tag genome relevance scores
│   ├── genome-tags.csv     # Tag genome descriptions
│   ├── models/             # Saved model artifacts (SVD, TF-IDF matrices)
│   └── notebooks/          # Notebooks for EDA and experimentation
├── docs/                   # General project documentation
├── scripts/                # Utility scripts 
├── apikey.py               # API keys (TMDb)
├── eda.py                  # Exploratory Data Analysis script
├── README.md               # Main project README
└── requirements.txt        # Root requirements file
```
