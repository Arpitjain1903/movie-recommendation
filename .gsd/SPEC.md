# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
A full-stack hybrid movie recommendation application that provides personalized movie suggestions to users. This system combines Collaborative Filtering and Content-Based Filtering models, leveraging the MovieLens 25M dataset and TMDb API, hosted cleanly behind a fast Python backend (FastAPI) and a minimal, responsive frontend (Streamlit).

## Goals
1. Collect data from MovieLens 25M dataset and enrich intelligently with the TMDb API.
2. Develop and train a Collaborative Filtering (SVD) model.
3. Develop a Content-Based Filtering (TF-IDF) model.
4. Merge them into a Hybrid model with adaptive weights based on number of user ratings.
5. Build a FastAPI backend for searching, recommending, storing, and rating movies.
6. Build a beautiful Streamlit multi-page frontend for the user journey.
7. Deploy the application for free to the Streamlit Community Cloud ($0 budget limit).

## Non-Goals (Out of Scope)
- Setup a relational backend production Database like PostgreSQL.
- Setup OAuth/Real user auth (will use basic session states).
- Complex social features like sharing and email notifications.

## Users
- Movie enthusiasts looking for personalized content to watch without a huge friction to setup logic.

## Constraints
- Needs to be highly optimized and entirely free to host.
- Recommendation latency must be under 300ms End-to-End.

## Success Criteria
- [ ] Trained Collaborative CF Model achieves RMSE < 0.87.
- [ ] Search functionality successfully returns fuzzy results with TMDb posters.
- [ ] End-to-end latency is verified to be under 300ms.
- [ ] Application is deployed and successfully accessible on the public internet.
