import streamlit as st
import datetime
import pandas as pd
import numpy as np
import cv2
import joblib
import pickle
from PIL import Image
import io
import os
import json
import datetime
import time
from streamlit_drawable_canvas import st_canvas

class JournalManager:
    def __init__(self, filename="journal_entries.json"):
        self.filename = filename
        # Create file if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def save_journal_entry(self, text):
        """Save today's journal entry to JSON file"""
        try:
            with open(self.filename, "r") as f:
                entries = json.load(f)
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            entries[date_str] = text
            with open(self.filename, "w") as f:
                json.dump(entries, f, indent=2)
            return True, self.filename
        except Exception as e:
            print("Error saving journal:", e)
            return False, None

    def load_today_entry(self):
        """Load today's journal entry if it exists"""
        try:
            with open(self.filename, "r") as f:
                entries = json.load(f)
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            return entries.get(date_str, "")
        except:
            return ""
# def photobooth():
#     st.title("📸 Photobooth")
    
#     start = st.button("Start Camera")
#     frame_placeholder = st.empty()
#     capture = st.checkbox("Capture Frame")

#     if start:
#         cap = cv2.VideoCapture(0)
#         st.info("Press 'Capture Frame' to take a snapshot")

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 st.warning("Failed to grab frame")
#                 break

#             frame = cv2.flip(frame, 1)
#             frame_placeholder.image(frame, channels="BGR")

#             if capture:
#                 st.success("Captured!")
#                 st.image(frame, caption="Captured Frame", channels="BGR")
#                 break

#             if not start:  # allow stopping
#                 break

#             time.sleep(0.05)

#         cap.release()

# Page configuration
st.set_page_config(
    page_title="Wellness Dashboard",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #e8f4f8 0%, #d4e7ed 100%);
        padding: 0rem 1rem;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Journal card */
    .journal-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        min-height: 80px;
    }
    
    /* Doodle card */
    .doodle-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        min-height: 80px;
    }
    
    /* Gradient card for inspiration */
    .inspiration-card {
        background: linear-gradient(135deg, #9c88ff 0%, #7dd3fc 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Assessment card */
    .assessment-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        min-height: 400px;
    }
    
    /* Camera card */
    .camera-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 12px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
        min-height: 80px;
    }
    
    /* Header styling */
    .header-date {
        color: #60a5fa;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Color palette */
    .color-dot {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-block;
        margin: 0 5px;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .color-dot:hover {
        border: 2px solid #333;
    }
    
    /* Button styling */
    .custom-button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(168, 85, 247, 0.3);
    }
    
    /* Mood slider */
    .mood-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Analysis results */
    .analysis-result {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 15px;
        margin: 5px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Status badges */
    .status-low { background: #fef3c7; color: #92400e; }
    .status-medium { background: #fed7aa; color: #c2410c; }
    .status-high { background: #fecaca; color: #dc2626; }
    .status-calm { background: #e0e7ff; color: #3730a3; }
    .status-minimal { background: #d1fae5; color: #065f46; }
    .status-good { background: #dcfce7; color: #166534; }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Greeting header */
    .greeting-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .greeting-date {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Backend Integration Classes and Functions

class BurnoutPredictor:
    def __init__(self):
        # Try to load the model, if not available, create a mock one
        try:
            self.model = joblib.load('burnout_model.joblib')
        except:
            # Create a mock model for demonstration
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(random_state=42)
            # Create dummy training data
            X_dummy = np.random.rand(100, 11)
            y_dummy = np.random.choice(['Low Risk', 'Medium Risk', 'High Risk'], 100)
            self.model.fit(X_dummy, y_dummy)
    
    def calculate_energy(self, sleep_hours, physical_activity, stress_level, mental_health_days):
        return (sleep_hours * 0.4) + (physical_activity * 0.3) - (stress_level * 0.3) - (0.1 * mental_health_days)
    
    def calculate_focus(self, job_satisfaction, productivity_score, burnout_level, work_hours):
        return (job_satisfaction * 0.3) + (productivity_score * 0.3) - (burnout_level * 0.2) + ((60 - abs(work_hours - 45)) / 60)
    
    def calculate_motivation(self, career_growth, manager_support, work_life_balance, has_mental_health_support, has_therapy_access):
        return (0.25 * career_growth + 0.25 * manager_support + 0.2 * work_life_balance + 
                0.15 * has_mental_health_support + 0.15 * has_therapy_access)
    
    def predict_burnout(self, input_data):
        # input_data should contain: Age, SleepHours, Energy, Focus, Motivation, JobSatisfaction,
        # StressLevel, ManagerSupportScore, RemoteWork_Yes, TeamSize, WorkHoursPerWeek
        try:
            prediction = self.model.predict([input_data])[0]
            probabilities = self.model.predict_proba([input_data])[0] if hasattr(self.model, 'predict_proba') else [0.7, 0.2, 0.1]
            return prediction, probabilities
        except:
            # Fallback prediction based on simple logic
            avg_score = np.mean(input_data)
            if avg_score >= 0.7:
                return "Low Risk", [0.8, 0.15, 0.05]
            elif avg_score >= 0.4:
                return "Medium Risk", [0.3, 0.6, 0.1]
            else:
                return "High Risk", [0.1, 0.3, 0.6]

class PhotoFilters:
    @staticmethod
    def apply_filter(frame, filter_name):
        kernel = np.ones((5, 5), np.uint8)
        if filter_name == "Grassau":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
            return cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)
        elif filter_name == "Average":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
            return cv2.cvtColor(th3, cv2.COLOR_GRAY2BGR)
        elif filter_name == "Gaussian":
            return cv2.GaussianBlur(frame, (21, 21), 0)
        elif filter_name == "Gradient":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
            return cv2.cvtColor(gradient, cv2.COLOR_GRAY2BGR)
        else:
            return frame

class JournalManager:
    @staticmethod
    def save_journal_entry(text, date=None):
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # In a real app, this would save to a database
        filename = f"journal_{date}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(f"Date: {date}\n")
                f.write(f"Entry: {text}\n")
            return True, filename
        except:
            return False, None
    
    @staticmethod
    def get_word_count(text):
        return len(text.split()) if text else 0
    
    @staticmethod
    def get_reading_time(text):
        word_count = JournalManager.get_word_count(text)
        # Average reading speed is 200-250 words per minute
        return max(1, word_count // 200)

# Initialize session state
if 'journal_text' not in st.session_state:
    st.session_state.journal_text = ""
if 'mood_level' not in st.session_state:
    st.session_state.mood_level = 3
if 'burnout_predictor' not in st.session_state:
    st.session_state.burnout_predictor = BurnoutPredictor()
if 'photo_filters' not in st.session_state:
    st.session_state.photo_filters = PhotoFilters()
if 'journal_manager' not in st.session_state:
    st.session_state.journal_manager = JournalManager()

# Camera state
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = "None"

def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <style>
            .greeting-header {
                color: #FF1493; /* Hot Pink */
                font-size: 32px;
                font-weight: bold;
            }
            .greeting-date {
                color: #555;
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="greeting-header">Good evening! 🌸</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="greeting-date">{datetime.datetime.now().strftime("%A, %B %d, %Y")}</div>', unsafe_allow_html=True)

    
    with col2:
        st.markdown("🔄 **Left-handed mode**")
    
    # First row - Mood tracking and Daily Inspiration
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>How are you feeling? 😊</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Mood slider
        mood = st.slider("", min_value=1, max_value=5, value=st.session_state.mood_level, 
                        help="Very Low - Low - Neutral - Good - Excellent", key="mood_slider")
        st.session_state.mood_level = mood
        
        mood_labels = ["Very Low", "Low", "Neutral", "Good", "Excellent"]
        st.markdown(f"**Current: {mood_labels[mood-1]}**")
        
        # Weekly mood dots
        st.markdown("**This week:**")
        dots_html = ""
        colors = ["#94a3b8", "#60a5fa", "#34d399", "#a78bfa", "#f472b6", "#fbbf24", "#60a5fa"]
        for color in colors:
            dots_html += f'<span class="color-dot" style="background-color: {color}; width: 15px; height: 15px; margin: 0 3px;"></span>'
        st.markdown(dots_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="inspiration-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: white;">Daily Inspiration</h3>
                <div style="display: flex; gap: 10px;">
                    <span style="color: white;">♡</span>
                    <span style="color: white;">↻</span>
                </div>
            </div>
            <br>
            <p style="font-size: 1.2rem; margin: 10px 0; color: white;">
                "Your positive energy is contagious. Keep shining! ✨"
            </p>
            <small style="color: rgba(255, 255, 255, 0.8);">Matched to your current mood</small>
            <div style="display: flex; justify-content: flex-end; margin-top: 15px;">
                <span style="color: white;">•••</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row - Journal and Doodle
    col1, col2 = st.columns([1, 1])
    
    # Session State init
# ========================
    if "journal_manager" not in st.session_state:
        st.session_state.journal_manager = JournalManager()

    if "journal_text" not in st.session_state:
        st.session_state.journal_text = st.session_state.journal_manager.load_today_entry()

# ========================
# Your existing UI code
# ========================
    with col1:
        st.markdown(f"""
    <div class="journal-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h3 style="margin: 0; color: #111827;">📖 Daily Journal</h3>
            <span class="header-date" style="color: #3B82F6;">{datetime.datetime.now().strftime("%d/%m/%Y")}</span>
        </div>
        <p style="color: #6b7280; margin-bottom: 8px; font-size: 0.9rem; line-height: 1.3;">
            Share your thoughts, feelings, or experiences...
        </p>
    </div>
    """, unsafe_allow_html=True)   

        journal_text = st.text_area(
        "",
        placeholder="Start writing your thoughts...",
        height=200,
        value=st.session_state.journal_text,
        key="journal",
        label_visibility="collapsed"
    )

        st.session_state.journal_text = journal_text

        col_stat1, col_stat2, col_stat3, col_save = st.columns([1, 1, 1, 1])
        with col_stat1:
            word_count = st.session_state.journal_manager.get_word_count(journal_text)
            st.caption(f"{word_count} words")
        with col_stat2:
            char_count = len(journal_text)
            st.caption(f"Characters: {char_count}")
        with col_stat3:
            reading_time = st.session_state.journal_manager.get_reading_time(journal_text)
            st.caption(f"~{reading_time} min read")
        with col_save:
            if st.button("💾 Save Entry", key="save_journal"):
                success, filename = st.session_state.journal_manager.save_journal_entry(journal_text)
                if success:
                    st.success(f"Entry saved to {filename}!")
                else:
                    st.error("Failed to save entry")

        st.markdown("**Need inspiration? Try these prompts:**")
        prompts = [
        "• What am I grateful for today?",
        "• What challenged me and how did I grow?",
        "• What made me smile today?"
    ]
        for prompt in prompts:
            st.markdown(f'<span style="color: #60a5fa; font-size: 0.9rem;">{prompt}</span>', unsafe_allow_html=True)
    # Create a placeholder at the top for the canvas
    # Initialize a counter in session_state
            if "clear_counter" not in st.session_state:
                st.session_state.clear_counter = 0
    with col2:
        with st.container():
        # --- Card style wrapper ---
            st.markdown("""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 10px;">
        """, unsafe_allow_html=True)

        # --- Card header ---
            st.markdown("""
        <h3 style="margin: 0;">🎨 Mindful Doodling</h3>
        <p style="color: #6b7280; margin-bottom: 15px;">
            Express your feelings through creative drawing
        </p>
        """, unsafe_allow_html=True)

        # --- Color picker ---
            color_options = {
            "Black": "#000000",
            "Purple": "#a855f7",
            "Blue": "#7dd3fc",
            "Yellow": "#fbbf24",
            "Green": "#34d399",
            "Pink": "#f472b6",
            "Gray": "#94a3b8",
            "Red": "#ef4444"
            }
            selected_color = st.selectbox("🎨 Choose Color", list(color_options.keys()))
            stroke_color = color_options[selected_color]

        # --- Brush size ---
            brush_size = st.slider("🖌️ Brush Size", min_value=1, max_value=20, value=5)

        # --- Drawing mode ---
            drawing_modes = ["freedraw", "line", "rect", "circle"]
            selected_mode = st.selectbox("✏️ Drawing Mode", drawing_modes)
            st.markdown(
    "<div style='font-size:0px;'>Canvas</div>", unsafe_allow_html=True
)  # invisible label for accessibility
        # --- Canvas ---
            canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=brush_size,
            stroke_color=stroke_color,
            background_color="#ffffff",
            height=250,
            width=400,
            drawing_mode=selected_mode,
            key=f"mindful_canvas_{st.session_state.clear_counter}"
            )

        # --- Buttons ---
            col_clear, col_save = st.columns(2)
            with col_clear:
                if st.button("🗑️ Clear"):
                    st.session_state.mindful_canvas_key=str(datetime.datetime.now())
            with col_save:
                if st.button("💾 Save Artwork"):
                    if canvas_result.image_data is not None:
                        filename = f"mindful_drawing_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        img = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
                        img.save(filename)
                        st.success(f"Saved as {filename}")

        # --- Tips ---
            st.markdown("""
        <div style="background: rgba(255, 248, 220, 0.8); padding: 10px; border-radius: 8px; margin-top: 15px;">
            <h4 style="color: #92400e; margin: 0 0 5px 0;">Mindful Drawing Tips</h4>
            <small style="color: #92400e;">
                • Focus on the present moment while drawing<br>
                • Let your emotions guide your strokes<br>
                • There's no right or wrong way to express yourself
            </small>
        </div>
        </div> <!-- Close card wrapper -->
        """, unsafe_allow_html=True)



    
    # Third row - Burnout Assessment and Emotion Detection
    col1, col2 = st.columns([1, 1])
    
    with col1:
       st.markdown("""
    <style>
    .assessment-card {
        background-color: white;
    border-radius: 8px;
    padding: 0.8rem 1rem; /* tighter spacing */
    margin-top: 0rem;     /* remove top margin */
    margin-bottom: 0.5rem;
    min-height: auto;     /* remove forced height */
    display: flex;
    flex-direction: column;
    justify-content: center;
    }
    .burnout-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #facc15;
        margin-bottom: 0.1rem;
    }
    .burnout-subtext {
        color: #9ca3af;
        font-size: 0.8rem;
        line-height: 1.2;
    }
    </style>
    <div class="assessment-card">
        <div class="burnout-header">⚠️ Burnout Assessment</div>
        <div class="burnout-subtext">
            Rate your current levels to assess burnout risk using AI prediction
        </div>
    </div>
    """, unsafe_allow_html=True)

        
        # Advanced burnout assessment with all model features
    with st.expander("📊 Advanced Assessment", expanded=True):
            col_left, col_right = st.columns(2)
            
            with col_left:
                age = st.slider("Age", min_value=18, max_value=65, value=30)
                sleep_hours = st.slider("Sleep Hours/night", min_value=3, max_value=12, value=7)
                job_satisfaction = st.slider("Job Satisfaction (1-10)", min_value=1, max_value=10, value=7)
                stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10, value=5)
                work_hours = st.slider("Work Hours/week", min_value=20, max_value=80, value=40)
            
            with col_right:
                physical_activity = st.slider("Physical Activity hrs/week", min_value=0, max_value=20, value=3)
                manager_support = st.slider("Manager Support (1-10)", min_value=1, max_value=10, value=6)
                team_size = st.slider("Team Size", min_value=1, max_value=20, value=5)
                remote_work = st.checkbox("Remote Work", value=False)
                mental_health_days = st.slider("Mental Health Days Off/month", min_value=0, max_value=10, value=1)
        
        # Calculate derived features using backend
    energy = st.session_state.burnout_predictor.calculate_energy(sleep_hours, physical_activity, stress_level, mental_health_days)
    focus = st.session_state.burnout_predictor.calculate_focus(job_satisfaction, 7, 3, work_hours)  # Mock productivity and burnout level
    motivation = st.session_state.burnout_predictor.calculate_motivation(6, manager_support, 7, 1, 0)  # Mock values
        
        # Display calculated metrics
    st.markdown("**Calculated Metrics:**")
    col_e, col_f, col_m = st.columns(3)
    with col_e:
        st.metric("Energy", f"{energy:.1f}")
        with col_f:
            st.metric("Focus", f"{focus:.1f}")
        with col_m:
            st.metric("Motivation", f"{motivation:.1f}")
        
        # Predict burnout using backend model
        if st.button("🔮 Predict Burnout Risk", key="predict_burnout"):
            # Prepare input for model
            input_features = [
                age, sleep_hours, energy, focus, motivation, job_satisfaction,
                stress_level, manager_support, int(remote_work), team_size, work_hours
            ]
            
            prediction, probabilities = st.session_state.burnout_predictor.predict_burnout(input_features)
            
            # Display results
            risk_colors = {"Low Risk": "#10b981", "Medium Risk": "#f59e0b", "High Risk": "#ef4444"}
            risk_messages = {
                "Low Risk": "Your levels indicate good overall wellbeing. Keep maintaining healthy habits!",
                "Medium Risk": "Consider taking breaks and focusing on self-care. Monitor your stress levels.",
                "High Risk": "Please prioritize rest and consider seeking professional support."
            }
            
            risk_color = risk_colors.get(prediction, "#6b7280")
            message = risk_messages.get(prediction, "Assessment complete.")
            
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid {risk_color};">
                <h4 style="color: {risk_color}; margin: 0 0 5px 0;">Prediction: {prediction}</h4>
                <p style="margin: 0; color: #6b7280;">{message}</p>
                <small style="color: #9ca3af;">Confidence: {max(probabilities)*100:.1f}%</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="camera-card">
            <h3>📷 Photobooth & Emotion Detection</h3>
            <p style="color: #6b7280; margin-bottom: 25px;">
                Capture photos with filters and analyze emotions
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter selection
        filter_options = ["None", "Grassau", "Average", "Gaussian", "Gradient"]
        selected_filter = st.selectbox("Choose Filter:", filter_options, key="filter_select")
        st.session_state.selected_filter = selected_filter
        
        # Camera controls
        col_start, col_stop = st.columns([1, 1])
        with col_start:
            if st.button("📹 Start Camera", key="start_camera"):
                st.session_state.camera_active = True
                st.success("Camera activated! (Simulated)")
        with col_stop:
            if st.button("⏹️ Stop Camera", key="stop_camera"):
                st.session_state.camera_active = False
        
        # Camera preview (simulated)
        if st.session_state.camera_active:
    # Set up OpenCV capture
            cap = cv2.VideoCapture(0)
            FRAME_WINDOW = st.empty()
            captured_frame = None

            st.info("Webcam is live. Press 'Capture Photo' below.")

    # Start webcam loop
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to access webcam.")
                    break

        # Apply filter
                selected_filter = st.session_state.selected_filter
                if selected_filter == "Grassau":
                    frame = cv2.stylization(frame, sigma_s=150, sigma_r=0.25)
                elif selected_filter == "Average":
                    frame = cv2.blur(frame, (15, 15))
                elif selected_filter == "Gaussian":
                    frame = cv2.GaussianBlur(frame, (15, 15), 0)
                elif selected_filter == "Gradient":
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)
                    frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

                frame = cv2.flip(frame, 1)
                FRAME_WINDOW.image(frame, channels="BGR")

        # Stop loop when capture is clicked
                captured_frame=None #initialize
                if st.button("📸 Capture Photo", key="photo_camera_section"):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"capture_{timestamp}.jpg"
                    captured_frame = frame.copy()
                    st.success(f"📸 Photo captured: {filename}")
    
                    cap.release()  # Safely placed inside the block
                    break

            time.sleep(0.03)


            if captured_frame is not None:
                st.image(captured_frame, caption="Captured Frame", channels="BGR")

        # Simulated emotion detection
            import random
            emotions = ["Calm & Focused", "Happy & Energetic", "Thoughtful", "Relaxed", "Motivated"]
            fatigue_levels = ["Low (2/10)", "Medium (5/10)", "High (8/10)"]
            stress_indicators = ["Minimal", "Moderate", "High"]

            detected_emotion = random.choice(emotions)
            detected_fatigue = random.choice(fatigue_levels)
            detected_stress = random.choice(stress_indicators)

            st.markdown("**Analysis Results:**")
            results = [
                ("Fatigue Level", detected_fatigue),
                ("Primary Emotion", detected_emotion),
                ("Stress Indicators", detected_stress)
            ]

            for label, value in results:
                st.markdown(f"""
            <div style="margin-bottom: 10px; padding: 10px; background: #f3f4f6; border-radius: 8px;">
                <strong>{label}:</strong> {value}
            </div>
            """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()

