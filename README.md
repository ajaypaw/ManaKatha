# ManaKatha – AI-Powered Telugu Story Sharing App

## Features
- Submit stories in Telugu (text or audio)
- Public story archive
- AI feedback (coming soon)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend (FastAPI):**
   ```bash
   uvicorn backend:app --reload
   ```

3. **Run the frontend (Streamlit):**
   ```bash
   streamlit run frontend.py
   ```

4. **Open the app:**
   - Streamlit UI: http://localhost:8501
   - Backend API: http://localhost:8000

## Next Steps
- Add MongoDB integration
- Implement AI sentiment, compliment, and rating
- Audio playback and transcription 

This means either:
- Python is not installed, or
- The `python` and `pip` commands are not in your system PATH, or
- You have multiple Python versions and the one referenced is missing.

---

## How to Fix

### 1. Check Python Installation

Open a new terminal and run:
```bash
python --version
```
or
```bash
python3 --version
```
If you get a version (e.g., Python 3.10.5), Python is installed.

### 2. Check pip Installation

Run:
```bash
pip --version
```
or
```bash
python -m pip --version
```
If you get a version, pip is installed.

### 3. If Not Installed

- Download and install Python from [python.org](https://www.python.org/downloads/).
- During installation, check the box that says “Add Python to PATH”.

### 4. Install Requirements

Once Python and pip are working, run:
```bash
pip install -r requirements.txt
```
or, if using python3:
```bash
python3 -m pip install -r requirements.txt
```

---

After this, you can proceed with:
```bash
uvicorn backend:app --reload
```
and
```bash
streamlit run frontend.py
```

---

If you run into any more errors, please copy the error message here and I’ll help you resolve it! 