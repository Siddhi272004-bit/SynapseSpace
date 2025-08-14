import streamlit as st
import cv2
import numpy as np
import joblib
from PIL import Image
import tempfile
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from datetime import datetime
import time

# Load model once
model = joblib.load("burnout_model.joblib")  # Replace with actual filename

# Streamlit UI
st.set_page_config(page_title="Mental Wellness Dashboard", layout="wide")
st.title("🧠 Mental Wellness Dashboard")

# Sidebar navigation
selected_feature = st.sidebar.selectbox("Select Feature", ["Burnout Prediction", "Photobooth", "Doodle Pad"])

# ---------------------------- Burnout Prediction ----------------------------
# ---------------------------- Burnout Prediction ----------------------------
if selected_feature == "Burnout Prediction":
    st.subheader("🔥 Burnout Prediction")

    age = st.slider("Age", 18, 65, 30)
    sleep_hours = st.slider("Sleep Hours per Night", 0, 12, 7)
    energy = st.slider("Energy (0-10)", 0, 10, 5)
    focus = st.slider("Focus (0-10)", 0, 10, 5)
    motivation = st.slider("Motivation (0-10)", 0, 10, 5)
    job_satisfaction = st.slider("Job Satisfaction (0-10)", 0, 10, 5)
    stress_level = st.slider("Stress Level (0-10)", 0, 10, 5)
    manager_support = st.slider("Manager Support Score (0-10)", 0, 10, 5)
    remote_work = st.selectbox("Do you work remotely?", ["No", "Yes"])
    team_size = st.slider("Team Size", 1, 50, 5)
    work_hours = st.slider("Work Hours per Week", 20, 80, 40)

    remote_encoded = 1 if remote_work == "Yes" else 0

    input_data = np.array([[age, sleep_hours, energy, focus, motivation,
                            job_satisfaction, stress_level, manager_support,
                            remote_encoded, team_size, work_hours]])

    if st.button("Predict Burnout"):
        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

        st.success(f"Prediction: {'🔥 Burnout Risk' if prediction == 1 else '✅ No Burnout Risk'}")
        st.metric("Burnout Probability", f"{prob:.2%}")

        # ROC Curve Visualization
        st.write("### Model Confidence Visualization")
        fpr, tpr, _ = roc_curve([0, 1], [0.2, prob])
        auc_val = auc(fpr, tpr)
        fig, ax = plt.subplots()
        ax.plot(fpr, tpr, label=f"AUC = {auc_val:.2f}")
        ax.plot([0, 1], [0, 1], 'k--')
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend()
        st.pyplot(fig)


# ---------------------------- Photobooth ----------------------------
elif selected_feature == "Photobooth":
    st.subheader("📸 Photobooth - Play Around with Filters!")

    filter_option = st.selectbox("Choose a filter:", ["None", "Sketch", "Cartoon"])
    detect_blue = st.checkbox("Enable blue object detection")

    if 'run' not in st.session_state:
        st.session_state.run = False

    start = st.button("Start Camera")
    stop = st.button("Stop Camera")
    capture = st.button("Capture")

    FRAME_WINDOW = st.image([])

    if start:
        st.session_state.run = True
    if stop:
        st.session_state.run = False

    cap = cv2.VideoCapture(0)

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame")
            break

        # --- Apply filter ---
        if filter_option == "Sketch":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            inv = 255 - gray
            grayblur = cv2.GaussianBlur(inv, (21, 21), 0)
            blur = 255 - grayblur
            inv_blur = 255 - blur
            sketch = cv2.divide(gray, inv_blur, scale=256.0)
            frame = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

        elif filter_option == "Cartoon":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(frame, 9, 250, 250)
            frame = cv2.bitwise_and(color, color, mask=edges)

        # --- Blue object detection ---
        if detect_blue:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([100, 150, 0])
            upper_blue = np.array([140, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, "Blue Object", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # --- Display the frame ---
        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Small delay to prevent crashing
        time.sleep(0.03)

    cap.release()

# ---------------------------- Doodle Pad ----------------------------


st.set_page_config(page_title="Doodle Pad", layout="wide")

st.subheader("🎨 Doodle Pad")
st.markdown("Draw using a **blue object** in front of the webcam.")

# Setup start button
if "doodle_active" not in st.session_state:
    st.session_state["doodle_active"] = False
if "canvas" not in st.session_state:
    st.session_state["canvas"] = None

start = st.button("▶️ Start Doodling")
stop = st.button("⏹️ Stop")

if start:
    st.session_state["doodle_active"] = True
if stop:
    st.session_state["doodle_active"] = False
    st.session_state["canvas"] = None

FRAME_WINDOW = st.image([])

if st.session_state["doodle_active"]:
    cap = cv2.VideoCapture(0)
    lower_blue = np.array([90, 60, 60])
    upper_blue = np.array([130, 255, 255])

    while st.session_state["doodle_active"]:
        ret, frame = cap.read()
        if not ret:
            st.error("Webcam not accessible.")
            break

        frame = cv2.flip(frame, 1)

        if st.session_state["canvas"] is None:
            st.session_state["canvas"] = np.zeros_like(frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 1000:
                x, y, w, h = cv2.boundingRect(c)
                cv2.circle(st.session_state["canvas"], (x + w // 2, y + h // 2), 8, (255, 255, 255), -1)

        combined = cv2.add(frame, st.session_state["canvas"])
        FRAME_WINDOW.image(combined, channels="BGR")

        # small delay to reduce CPU usage
        time.sleep(0.03)
    cap.release()
