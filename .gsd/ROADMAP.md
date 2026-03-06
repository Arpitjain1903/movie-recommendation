# ROADMAP.md

> **Current Phase**: Phase 2
> **Milestone**: v1.0

## Must-Haves (from SPEC)
- [/] Data Collection & Preprocessing (MovieLens + TMDb)
- [ ] Hybrid Recommendation Model (CF + Content-Based)
- [ ] FastAPI Backend Database & Service Structure
- [ ] Unified Streamlit Web Interface
- [ ] Fully Deployed Free Hosting (Streamlit Cloud)

## Phases

### Phase 1: Data Collection & Setup
**Status**: ✅ Complete
**Objective**: Get the data, explore it, and prepare the project skeleton.

### Phase 2: Data Preprocessing & TMDb Enrichment
**Status**: 🔄 In Progress
**Objective**: Clean data and enrich movies with TMDb metadata and posters. Prepare feature representations.

### Phase 3: Collaborative Filtering Model (SVD)
**Status**: ⬜ Not Started
**Objective**: Train and evaluate an SVD model using the Surprise library.

### Phase 4: Content-Based Filtering Model (TF-IDF)
**Status**: ⬜ Not Started
**Objective**: Construct a TF-IDF Title/Genre-Based Recommendation index and compute document similarity.

### Phase 5: Hybrid Model Combination
**Status**: ⬜ Not Started
**Objective**: Implement adaptive blending logic mixing the SVD user-based model and the Content similarities.

### Phase 6: FastAPI Backend
**Status**: ⬜ Not Started
**Objective**: Wrap model inference logic into a real-time, high-performance structured HTTP service setup.

### Phase 7: Streamlit Frontend
**Status**: ⬜ Not Started
**Objective**: Build out User Search, UI components, movie visualizations and rating states entirely in python via Streamlit.

### Phase 8: Integration & End-to-End Testing
**Status**: ⬜ Not Started
**Objective**: Test latency, handle errors safely, integrate pieces directly to each other seamlessly, and provide fallback UI images for dead links.

### Phase 9: Deployment to Streamlit Community Cloud
**Status**: ⬜ Not Started
**Objective**: Manage environment packages and host solution securely online using zero-cost cloud.
