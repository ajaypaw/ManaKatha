from fastapi import FastAPI, UploadFile, File, Form, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import random
from fastapi.staticfiles import StaticFiles
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from fastapi import HTTPException
from passlib.hash import bcrypt
from fastapi.responses import FileResponse

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://ajaypawar113307:GVN7uf5k7sAewEVF@cluster0.jypfmdn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URL)
db = client["manakatha"]
stories_col = db["stories"]
users_col = db["users"]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Load IndicBERT/MuRIL model for sentiment (placeholder: use a real model path or name)
try:
    sentiment_tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-bert-sentiment")
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("ai4bharat/indic-bert-sentiment")
    sentiment_model.eval()
except Exception as e:
    sentiment_tokenizer = None
    sentiment_model = None
    print("Sentiment model not loaded:", e)

AVATAR_DIR = "avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)
app.mount("/avatars", StaticFiles(directory=AVATAR_DIR), name="avatars")

@app.post("/register/")
def register(username: str = Form(...), password: str = Form(...)):
    if users_col.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = bcrypt.hash(password)
    user = {"username": username, "password": hashed}
    result = users_col.insert_one(user)
    return {"message": "Registered successfully", "user_id": str(result.inserted_id)}

@app.post("/login/")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_col.find_one({"username": username})
    if not user or not bcrypt.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": str(user["_id"])}

@app.post("/submit_story/")
def submit_story(
    user_id: str = Form(...),
    text: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    title: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    is_public: bool = Form(True)
):
    audio_path = None
    if audio:
        audio_path = os.path.join(UPLOAD_DIR, audio.filename)
        with open(audio_path, "wb") as f:
            f.write(audio.file.read())
    # Check user exists
    if not users_col.find_one({"_id": ObjectId(user_id)}):
        raise HTTPException(status_code=401, detail="Invalid user")
    story = {
        "user_id": user_id,
        "text": text,
        "audio_path": audio_path,
        "title": title,
        "tags": tags.split(",") if tags else [],
        "is_public": is_public
    }
    result = stories_col.insert_one(story)
    story["_id"] = str(result.inserted_id)
    return {"message": "Story submitted!", "story": story}

@app.post("/upload_avatar/")
def upload_avatar(user_id: str = Form(...), avatar: UploadFile = File(...)):
    # Check user exists
    user = users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    avatar_path = os.path.join(AVATAR_DIR, f"{user_id}_{avatar.filename}")
    with open(avatar_path, "wb") as f:
        f.write(avatar.file.read())
    users_col.update_one({"_id": ObjectId(user_id)}, {"$set": {"avatar_path": avatar_path}})
    return {"message": "Avatar uploaded!", "avatar_url": f"/avatars/{os.path.basename(avatar_path)}"}

@app.get("/avatar/{user_id}")
def get_avatar(user_id: str):
    user = users_col.find_one({"_id": ObjectId(user_id)})
    if not user or "avatar_path" not in user:
        # Return a simple text response instead of trying to serve a non-existent file
        from fastapi.responses import Response
        return Response(content="No avatar available", media_type="text/plain")
    return FileResponse(user["avatar_path"])

@app.get("/stories/")
def get_stories(public_only: bool = True):
    query = {"is_public": True} if public_only else {}
    stories = list(stories_col.find(query))
    for s in stories:
        s["_id"] = str(s["_id"])
    return stories

@app.post("/analyze_story/")
def analyze_story(text: str = Body(...)):
    # Real sentiment analysis if model is loaded
    if sentiment_model and sentiment_tokenizer and text:
        inputs = sentiment_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = sentiment_model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)[0]
            sentiment_idx = torch.argmax(scores).item()
            sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
            sentiment = sentiment_map.get(sentiment_idx, "neutral")
            confidence = scores[sentiment_idx].item()
    else:
        # Fallback logic
        sentiment = "neutral"
        confidence = 0.5

    # Compliment templates (expand for more variety)
    compliments = [
        "మీ కథ చాలా బాగుంది!",
        "మీరు అద్భుతంగా రాశారు!",
        "కథలో భావోద్వేగం బాగా వ్యక్తమైంది!",
        "మీ రచనకు అభినందనలు!",
        "మీ కథలోని సందేశం హృదయాన్ని తాకింది!"
    ]
    compliment = random.choice(compliments)

    # Improved rating: based on confidence and text length
    base = int(confidence * 10)
    length_bonus = min(len(text) // 100, 2)  # up to +2 for long stories
    rating = min(10, base + length_bonus)

    return {
        "sentiment": sentiment,
        "compliment": compliment,
        "rating": rating
    }

@app.patch("/edit_story/{story_id}")
def edit_story(story_id: str, request: Request):
    data = request.json() if hasattr(request, 'json') else {}
    user_id = data.get("user_id")
    story = stories_col.find_one({"_id": ObjectId(story_id)})
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_fields = {k: v for k, v in data.items() if k in ["text", "title", "tags", "is_public"]}
    if update_fields:
        stories_col.update_one({"_id": ObjectId(story_id)}, {"$set": update_fields})
    return {"message": "Story updated!"}

@app.delete("/delete_story/{story_id}")
def delete_story(story_id: str, user_id: str):
    story = stories_col.find_one({"_id": ObjectId(story_id)})
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    stories_col.delete_one({"_id": ObjectId(story_id)})
    return {"message": "Story deleted!"} 