import streamlit as st
import requests
import time
from PIL import Image
import io

BACKEND_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="ManaKatha - తెలుగు కథలు",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional design
st.markdown('''
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Header Styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .main-header h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        background: linear-gradient(45deg, #11998e, #38ef7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 0;
    }
    
    /* Card Styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(17, 153, 142, 0.6);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #11998e;
        box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stError {
        background: linear-gradient(45deg, #f44336, #d32f2f);
        color: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Story Card Styling */
    .story-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .story-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Avatar Styling */
    .avatar-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .avatar-image {
        border-radius: 50%;
        border: 3px solid #11998e;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .custom-card {
            padding: 1.5rem;
        }
    }
    
    /* Animation for loading */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #0f8a7a, #2ed573);
    }
    </style>
''', unsafe_allow_html=True)

# Session state for user
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

def get_avatar_url(user_id):
    return f"{BACKEND_URL}/avatars/{user_id}_{user_id}.png"

def fetch_avatar(user_id):
    try:
        resp = requests.get(f"{BACKEND_URL}/avatar/{user_id}")
        if resp.ok:
            return Image.open(io.BytesIO(resp.content))
    except Exception:
        pass
    return None

# Main header
st.markdown('''
<div class="main-header fade-in">
    <h1>📚 ManaKatha</h1>
    <p>Share and discover beautiful Telugu stories</p>
</div>
''', unsafe_allow_html=True)

# Sidebar with modern design
with st.sidebar:
    st.markdown('''
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #11998e; font-family: 'Poppins', sans-serif;">🎭</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.session_state.user_id:
        # User profile section
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        avatar_img = fetch_avatar(st.session_state.user_id)
        if avatar_img:
            st.image(avatar_img, width=80, use_column_width=True)
        
        st.markdown(f'''
        <div style="text-align: center; margin: 1rem 0;">
            <h3 style="color: #11998e; font-family: 'Poppins', sans-serif;">Welcome back!</h3>
            <p style="color: #666; font-family: 'Poppins', sans-serif;">{st.session_state.username}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Avatar upload
        with st.expander("📷 Update Avatar", expanded=False):
        with st.form("avatar_form"):
                avatar_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], key="avatar_upload")
                submitted = st.form_submit_button("Upload Avatar", use_container_width=True)
            if submitted and avatar_file:
                files = {"avatar": avatar_file}
                data = {"user_id": st.session_state.user_id}
                resp = requests.post(f"{BACKEND_URL}/upload_avatar/", data=data, files=files)
                if resp.ok:
                        st.success("Avatar uploaded successfully! ✨")
                        st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.success("Logged out successfully!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="custom-card">
            <div style="text-align: center;">
                <h3 style="color: #11998e; font-family: 'Poppins', sans-serif;">👋 Welcome!</h3>
                <p style="color: #666; font-family: 'Poppins', sans-serif;">Please log in to start sharing your stories</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Navigation menu
menu = st.sidebar.selectbox(
    "📖 Navigation",
    ["🏠 Home", "👤 Profile", "🔐 Login/Register", "✍️ Submit Story", "📚 Story Archive"],
    format_func=lambda x: x.split(" ", 1)[1] if " " in x else x
)

def get_ai_feedback(text):
    if not text:
        return None
    with st.spinner("🤖 Analyzing your story..."):
        resp = requests.post(f"{BACKEND_URL}/analyze_story/", json={"text": text})
    if resp.ok:
        return resp.json()
    return None

def login_form():
    st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #11998e; font-family: \'Poppins\', sans-serif;">🔐 Login</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username", key="login_user")
        password = st.text_input("🔒 Password", type="password", key="login_pass")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("Login", use_container_width=True):
                if username and password:
        data = {"username": username, "password": password}
                    with st.spinner("🔐 Logging in..."):
            resp = requests.post(f"{BACKEND_URL}/login/", data=data)
        if resp.ok:
            st.session_state.user_id = resp.json()["user_id"]
            st.session_state.username = username
                        st.success("🎉 Login successful!")
            time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Login failed. Please check your credentials.")
        else:
                    st.warning("⚠️ Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

def register_form():
    st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #11998e; font-family: \'Poppins\', sans-serif;">📝 Register</h2>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        username = st.text_input("👤 Username", key="reg_user")
        password = st.text_input("🔒 Password", type="password", key="reg_pass")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", key="confirm_pass")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("Register", use_container_width=True):
                if username and password and confirm_password:
                    if password == confirm_password:
        data = {"username": username, "password": password}
                        with st.spinner("📝 Creating account..."):
            resp = requests.post(f"{BACKEND_URL}/register/", data=data)
        if resp.ok:
                            st.success("🎉 Registration successful! Please log in.")
                        else:
                            st.error("❌ Registration failed. Username might already exist.")
                    else:
                        st.error("❌ Passwords don't match.")
        else:
                    st.warning("⚠️ Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

def sentiment_emoji(sentiment):
    if sentiment == "positive" or sentiment == "happy":
        return "😍"
    elif sentiment == "negative" or sentiment == "sad":
        return "😢"
    elif sentiment == "inspiring":
        return "👏"
    else:
        return "😐"

# Home page
if menu == "🏠 Home":
    st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
    st.markdown('''
    <h1 style="text-align: center; color: #11998e; font-family: 'Poppins', sans-serif; margin-bottom: 2rem;">
        🌟 Welcome to ManaKatha 🌟
    </h1>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <h3 style="color: #11998e;">📖</h3>
            <h4 style="color: #333;">Share Stories</h4>
            <p style="color: #666;">Share your beautiful Telugu stories with the community</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <h3 style="color: #11998e;">🤖</h3>
            <h4 style="color: #333;">AI Analysis</h4>
            <p style="color: #666;">Get AI-powered feedback on your stories</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div style="text-align: center; padding: 1rem;">
            <h3 style="color: #11998e;">👥</h3>
            <h4 style="color: #333;">Connect</h4>
            <p style="color: #666;">Connect with fellow Telugu story enthusiasts</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Profile page
elif menu == "👤 Profile":
    if not st.session_state.user_id:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.warning("⚠️ Please log in to view your profile.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #11998e; font-family: \'Poppins\', sans-serif;">👤 Your Profile</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
        avatar_img = fetch_avatar(st.session_state.user_id)
        if avatar_img:
                st.image(avatar_img, width=150, use_column_width=True)
            else:
                st.markdown('''
                <div style="text-align: center; padding: 2rem; background: #f0f0f0; border-radius: 50%; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center;">
                    <h1 style="font-size: 3rem;">👤</h1>
                </div>
                ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div style="padding: 1rem;">
                <h3 style="color: #11998e;">{st.session_state.username}</h3>
                <p style="color: #666;">Member since today</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Fetch user's stories for count
        params = {"public_only": "false"}
        response = requests.get(f"{BACKEND_URL}/stories/", params=params)
        if response.ok:
            stories = response.json()
            user_stories = [s for s in stories if s.get("user_id") == st.session_state.user_id]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 Stories", len(user_stories))
            with col2:
                public_stories = [s for s in user_stories if s.get("is_public", True)]
                st.metric("🌍 Public", len(public_stories))
            with col3:
                private_stories = [s for s in user_stories if not s.get("is_public", True)]
                st.metric("🔒 Private", len(private_stories))
        
        st.markdown('</div>', unsafe_allow_html=True)

# Login/Register page
elif menu == "🔐 Login/Register":
    if not st.session_state.user_id:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            login_form()
        
        with tab2:
            register_form()

# Submit Story page
elif menu == "✍️ Submit Story":
    if not st.session_state.user_id:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.warning("⚠️ Please log in to submit a story.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #11998e; font-family: \'Poppins\', sans-serif;">✍️ Share Your Story</h2>', unsafe_allow_html=True)
        
        with st.form("story_form"):
        col1, col2 = st.columns(2)
            
        with col1:
                title = st.text_input("📝 Title (optional)")
                tags = st.text_input("🏷️ Tags (comma separated)")
                is_public = st.checkbox("🌍 Make story public", value=True)
            
        with col2:
                text = st.text_area("📖 Write your story in Telugu", height=200)
                audio = st.file_uploader("🎵 Or upload audio story", type=["mp3", "wav", "m4a"])
            
            # Preview section
        if text or audio:
            st.markdown("---")
                st.markdown('<h4 style="color: #11998e;">👀 Preview</h4>', unsafe_allow_html=True)
                
            if title:
                    st.markdown(f"**Title:** {title}")
            if tags:
                    st.markdown(f"**Tags:** {tags}")
            if text:
                    st.markdown(f"**Story:** {text}")
            if audio:
                st.audio(audio)
                st.markdown(f"**Visibility:** {'🌍 Public' if is_public else '🔒 Private'}")
            
            # Submit button
        submit_disabled = not (text or audio)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.form_submit_button("🚀 Submit Story", disabled=submit_disabled, use_container_width=True):
            files = {"audio": audio} if audio else None
            data = {
                "user_id": st.session_state.user_id,
                "title": title,
                "tags": tags,
                "text": text,
                "is_public": str(is_public)
            }
            try:
                        with st.spinner("📤 Submitting your story..."):
                    response = requests.post(f"{BACKEND_URL}/submit_story/", data=data, files=files)
                if response.ok:
                            st.success("🎉 Story submitted successfully!")
                    if text:
                        ai = get_ai_feedback(text)
                        if ai:
                            emoji = sentiment_emoji(ai['sentiment'])
                                    st.info(f"🤖 Sentiment: {ai['sentiment']} {emoji}")
                                    st.success(f"💬 {ai['compliment']}")
                                    st.markdown(f"⭐ Rating: {ai['rating']} / 10")
                            st.rerun()
                else:
                            st.error(f"❌ Failed to submit story: {response.text}")
            except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Story Archive page
elif menu == "📚 Story Archive":
    st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #11998e; font-family: \'Poppins\', sans-serif;">📚 Story Archive</h2>', unsafe_allow_html=True)
    
    show_private = False
    if st.session_state.user_id:
        show_private = st.checkbox("🔒 Show my private stories", value=False)
    
    params = {"public_only": "false" if show_private and st.session_state.user_id else "true"}
    
    with st.spinner("📚 Loading stories..."):
        response = requests.get(f"{BACKEND_URL}/stories/", params=params)
    
    if response.ok:
        stories = response.json()
        
        # Search functionality
        search = st.text_input("🔍 Search by title or tag")
        if search:
            stories = [s for s in stories if search.lower() in (s.get("title", "").lower() + " ".join(s.get("tags", [])).lower())]
        
        # Group by date
        from bson.objectid import ObjectId
        from datetime import datetime
        for s in stories:
            if "_id" in s:
                try:
                    s["date"] = datetime.fromtimestamp(ObjectId(s["_id"]).generation_time.timestamp()).strftime("%Y-%m-%d")
                except Exception:
                    s["date"] = "Unknown"
            else:
                s["date"] = "Unknown"
        
        # Story of the Day
        import random
        sotd = None
        if stories:
            sotd = random.choice([s for s in stories if s.get("is_public", True)])
        
        if sotd:
            st.markdown('<div class="story-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: #11998e;">🌟 Story of the Day</h3>', unsafe_allow_html=True)
            st.markdown(f"**{sotd.get('title', 'Untitled')}**")
            st.markdown(f"👤 By: {sotd.get('user_id', 'Unknown')} | 📅 {sotd.get('date', 'Unknown')}")
            if sotd.get("tags"):
                st.markdown(f"🏷️ {', '.join(sotd.get('tags', []))}")
            st.markdown(f"📖 {sotd.get('text', '[Audio only story]')}")
            
            if sotd.get("audio_path"):
                audio_url = f"{BACKEND_URL}/uploads/{sotd['audio_path'].split('/')[-1]}"
                st.audio(audio_url)
            
            if sotd.get("text"):
                ai = get_ai_feedback(sotd["text"])
                if ai:
                    emoji = sentiment_emoji(ai['sentiment'])
                    st.info(f"🤖 Sentiment: {ai['sentiment']} {emoji}")
                    st.success(f"💬 {ai['compliment']}")
                    st.markdown(f"⭐ Rating: {ai['rating']} / 10")
            st.markdown('</div>')
        
        # Group stories by date
        stories_by_date = {}
        for s in stories:
            if sotd and s["_id"] == sotd["_id"]:
                continue  # skip SOTD in main list
            stories_by_date.setdefault(s["date"], []).append(s)
        
        for date in sorted(stories_by_date.keys(), reverse=True):
            st.markdown(f'<h4 style="color: #11998e;">📅 {date}</h4>', unsafe_allow_html=True)
            
            for s in stories_by_date[date]:
                st.markdown('<div class="story-card">', unsafe_allow_html=True)
                st.markdown(f"**{s.get('title', 'Untitled')}**")
                st.markdown(f"👤 By: {s.get('user_id', 'Unknown')}")
                
                avatar_img = fetch_avatar(s.get('user_id'))
                if avatar_img:
                    st.image(avatar_img, width=50)
                
                if s.get("tags"):
                    st.markdown(f"🏷️ {', '.join(s.get('tags', []))}")
                
                st.markdown(f"📖 {s.get('text', '[Audio only story]')}")
                
                if s.get("audio_path"):
                    audio_url = f"{BACKEND_URL}/uploads/{s['audio_path'].split('/')[-1]}"
                    st.audio(audio_url)
                
                if s.get("text"):
                    ai = get_ai_feedback(s["text"])
                    if ai:
                        emoji = sentiment_emoji(ai['sentiment'])
                        st.info(f"🤖 Sentiment: {ai['sentiment']} {emoji}")
                        st.success(f"💬 {ai['compliment']}")
                        st.markdown(f"⭐ Rating: {ai['rating']} / 10")
                
                # Edit/Delete for own stories
                if st.session_state.user_id and s.get("user_id") == st.session_state.user_id:
                    with st.expander("✏️ Edit/Delete Story"):
                        new_title = st.text_input(f"Edit Title", value=s.get("title", ""))
                        new_text = st.text_area(f"Edit Text", value=s.get("text", ""))
                        new_tags = st.text_input(f"Edit Tags", value=", ".join(s.get("tags", [])))
                        new_is_public = st.checkbox(f"Public", value=s.get("is_public", True))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"💾 Save Changes"):
                            patch_data = {
                                "user_id": st.session_state.user_id,
                                "title": new_title,
                                "text": new_text,
                                "tags": [t.strip() for t in new_tags.split(",")],
                                "is_public": new_is_public
                            }
                            try:
                                resp = requests.patch(f"{BACKEND_URL}/edit_story/{s['_id']}", json=patch_data)
                                if resp.ok:
                                        st.success("✅ Story updated!")
                                        st.rerun()
                                else:
                                        st.error(f"❌ Failed to update: {resp.text}")
                            except Exception as e:
                                    st.error(f"❌ Error: {e}")
                        
                        with col2:
                            if st.button(f"🗑️ Delete Story"):
                                if st.confirm("Are you sure you want to delete this story?"):
                                try:
                                    resp = requests.delete(f"{BACKEND_URL}/delete_story/{s['_id']}?user_id={st.session_state.user_id}")
                                    if resp.ok:
                                            st.success("✅ Story deleted!")
                                            st.rerun()
                                    else:
                                            st.error(f"❌ Failed to delete: {resp.text}")
                                except Exception as e:
                                        st.error(f"❌ Error: {e}")
                
                st.markdown('</div>')
    else:
        st.error(f"❌ Could not fetch stories: {response.text}")
    
    st.markdown('</div>', unsafe_allow_html=True) 