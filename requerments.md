# 🧾 requirements.md – ManaKatha (Telugu Story Sharing App)

---

## 📌 Project Title:
**ManaKatha – AI-Powered Telugu Story Sharing App (Text + Audio)**

---

## 🎯 Purpose:
To create a culturally rich, low-bandwidth-friendly application where users can submit **personal stories in Telugu** as **written text or audio**, and receive **AI-generated appreciation, sentiment response, and ratings**. It also functions as a **corpus collection engine** to aid AI training in Telugu.

---

## 🧱 Functional Requirements (MVP)

### 📝 Story Submission
- [x] Users can write their story in Telugu using an on-screen keyboard.
- [x] Users can record or upload an audio story.
- [x] Optional: Add title and tags (e.g., love, friendship, village life).
- [x] Option to set story as **Public** or **Private**.

### 🎙️ Audio Handling
- [x] Audio stories are stored securely.
- [ ] Optional future feature: Transcribe Telugu audio using open-source ASR models like **IndicWav2Vec** or **Bhashini**.

### 🤖 AI Appreciation Engine
- [x] Analyze story sentiment (happy, sad, inspiring, etc.)
- [x] Generate compliment in Telugu using templates.
- [x] Display emoji-based response (😍, 😢, 👏).

### 🌟 AI Rating Engine
- [x] Rate stories on:
  - Emotion
  - Clarity (from text or transcribed audio)
  - Uniqueness
- [x] Show star rating or score (out of 10).

### 📚 Story Archive
- [x] Public archive of shared stories.
- [x] Filter by category or tags.
- [ ] Play audio or read text versions.
- [ ] Show "Story of the Day" (optional).

---

## 🛠️ Technical Requirements

### Frontend
- [x] Built using **Streamlit**
- [x] Input support for **Telugu typing**
- [x] Audio recording/upload via browser
- [x] Responsive design for mobile and low-end devices

### Backend
- [ ] Use **FastAPI** or **Flask** for story submission API
- [ ] Secure audio and text storage
- [ ] Endpoints for:
  - Submit story (text/audio)
  - Trigger AI response
  - Fetch stories

### Database
- [x] MongoDB or Firebase:
  - Store story text/audio paths
  - Metadata (user ID, tags, time)
  - AI scores/responses

### AI Layer
- [x] Sentiment analysis using **IndicBERT** / **MuRIL**
- [x] Compliment generator with pre-written Telugu phrases
- [x] Custom rating logic using embedding-based analysis
- [ ] Optional: Use **CLIP**/**BERT** similarity for emotion scoring
- [ ] Audio transcription using **IndicWav2Vec**, **Bhashini-ASR**

### Hosting
- [x] **Hugging Face Spaces** for MVP deployment
- [ ] Offline-first support via local caching (optional)
- [ ] Optional future hosting on **Vercel/Firebase**

---

## 🧪 Testing Requirements

- [x] Story submission (text + audio)
- [x] AI response output test
- [x] Sentiment accuracy for Telugu input
- [ ] Offline simulation testing (2G/3G network conditions)
- [ ] Functional testing on mobile browsers

---

## 🔒 Non-Functional Requirements

- [x] Fully open-source stack (no ChatGPT/OpenAI/Bard)
- [x] Telugu-focused UX with native fonts
- [x] Works in low bandwidth and offline-first design
- [x] Scalable backend for story storage and AI processing
- [x] GDPR-style data privacy (user-owned content)

---

## 📦 Final Deliverables

- [ ] Public Git Repo with:
  - `README.md`
  - `REPORT.md`
  - `requirements.md`
  - `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`
- [ ] Live App hosted on Hugging Face
- [ ] Demo Video (5–7 min)
- [ ] Final corpus dataset export (stories, tags, emotion)

---

## ✅ Success Criteria

- [ ] Collect **100+ unique Telugu stories**
- [ ] At least 25 audio stories submitted
- [ ] AI responses rated “realistic” by >75% of users
- [ ] Minimum 1000+ Telugu sentences added to corpus
- [ ] Mobile users able to submit successfully on 3G

---
