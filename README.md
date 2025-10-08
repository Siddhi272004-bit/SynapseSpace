# 🌸 SynapseSpace – Wellness Dashboard

An interactive **mental wellness dashboard** built with [Streamlit](https://streamlit.io/) to support **self-reflection, journaling, burnout assessment, and emotion tracking**.  
It combines journaling, mindful doodling, AI-based burnout risk prediction, and a webcam photobooth with emotion analysis.

---

🔗 Live Demo

**🚀 Try it here:** [SynapseSpace (Deployed App)](https://synapsespace-zxwjmahsjydlea5saa8jlk.streamlit.app/)

---

## ✨ Features

- **📖 Daily Journal** – Write and save your thoughts; auto-saves by date. Word count and estimated reading time included.  
- **🎨 Mindful Doodling** – Draw on a canvas with custom brushes, colors, and shapes. Save your artwork for reflection.  
- **😊 Mood Tracking** – Rate your daily mood (1–5 scale) and visualize trends across the week.  
- **⚠️ Burnout Assessment** – Advanced sliders to input lifestyle & workplace metrics → AI model predicts burnout risk (Low, Medium, High).  
- **📷 Photobooth & Emotion Detection** – Capture webcam snapshots with filters (Gaussian, Average, Gradient, etc.) and simulated fatigue/emotion analysis.  
- **🌟 Daily Inspiration** – Motivational quote matched to your mood.  

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend/ML**: Python, Scikit-learn (RandomForest mock burnout predictor)  
- **Other Libraries**:  
  - `opencv-python` (camera + filters)  
  - `numpy`, `pandas` (data ops)  
  - `joblib` (model persistence)  
  - `PIL` (image saving)  
  - `streamlit-drawable-canvas` (doodling)  

---

## 📂 Project Structure
├── streamlit_app.py # Main application
├── burnout_model.joblib # (optional) Pretrained burnout predictor model
├── journal_entries.json # Saved journal entries (auto-created)
├── mindful_drawing_.png # Saved doodles
├── capture_.jpg # Saved webcam captures
└── requirements.txt # Dependencies (create this file, see below)



---

## ⚙️ Installation

1.📥 **Clone the repo**
   ```bash
   git clone https://github.com/Siddhi272004-bit/SynapseSpace
   Create a virtual environment (recommended)
# 2.🛠️ Create & activate a virtual environment
python -m venv venv
# On Mac/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# 3.📦 Install dependencies
pip install -r requirements.txt

# 4.🚀 Run the Streamlit app
streamlit run streamlit_app.py
