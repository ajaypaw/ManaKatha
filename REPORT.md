# ManaKatha – Project Report

## Overview
ManaKatha is an AI-powered Telugu story sharing app that enables users to submit personal stories in Telugu as text or audio. The platform provides AI-generated appreciation, sentiment analysis, and ratings, and serves as a corpus collection engine for Telugu AI research.

## Features
- **Story Submission:** Users can submit stories in Telugu (text or audio), add titles and tags, and choose public/private visibility.
- **Audio Handling:** Audio stories are securely stored and can be played back in the archive.
- **AI Appreciation Engine:** Stories receive AI-generated sentiment, Telugu compliments, and emoji-based responses.
- **AI Rating Engine:** Stories are rated on emotion, clarity, and uniqueness.
- **Story Archive:** Public archive with search, filtering, grouping by date, and “Story of the Day.”
- **User System:** Registration, login, profile with avatar, and user-specific story management (edit/delete).
- **Mobile-Friendly:** Responsive design for mobile and low-end devices.

## Technical Stack
- **Frontend:** Streamlit (Python), responsive UI, mobile-optimized, avatar upload.
- **Backend:** FastAPI (Python), RESTful API, MongoDB for storage, secure file handling.
- **Database:** MongoDB (stories, users, metadata, AI results).
- **AI Layer:** Sentiment analysis using IndicBERT/MuRIL, compliment generator, custom rating logic.
- **Audio:** Upload, storage, and playback of audio stories.
- **Authentication:** Username/password with hashed storage, session management.
- **Deployment:** Ready for Hugging Face Spaces or similar platforms.

## Usage

### Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start MongoDB (local or cloud).
3. Run backend:
   ```
   uvicorn backend:app --reload
   ```
4. Run frontend:
   ```
   streamlit run frontend.py
   ```
5. Open [http://localhost:8501](http://localhost:8501) in your browser.

### User Flows
- Register/login, upload avatar, submit stories, view and manage archive, receive AI feedback.

## Future Work
- Audio transcription (IndicWav2Vec/Bhashini)
- Offline-first support
- Corpus export tools
- Advanced emotion scoring (CLIP/BERT)
- Deployment scripts and further testing

--- 