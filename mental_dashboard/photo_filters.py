import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

# Global state
current_filter = "None"
entered_center_time = None
photo_taken = False

def apply_filter(frame, name):
    kernel = np.ones((5, 5), np.uint8)
    if name == "Grassau":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
        frame = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)
    elif name == "Average":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
        frame = cv2.cvtColor(th3, cv2.COLOR_GRAY2BGR)
    elif name == "Gaussian":
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
    elif name == "Gradient":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
        frame = cv2.cvtColor(gradient, cv2.COLOR_GRAY2BGR)
    return frame

def show_feedback(message, color="lightgreen"):
    feedback_label.config(text=message, fg=color)
    root.after(2000, lambda: feedback_label.config(text=""))

def update_frame():
    global entered_center_time, photo_taken

    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    blue_detected = False
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        M = cv2.moments(largest)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            h_, w_ = frame.shape[:2]
            fx, fy = w_ // 2, h_ // 2
            zone = 100
            cv2.rectangle(frame, (fx - zone, fy - zone), (fx + zone, fy + zone), (255, 0, 255), 2)

            in_center = abs(cx - fx) < zone and abs(cy - fy) < zone
            blue_detected = True

            if in_center:
                if entered_center_time is None:
                    entered_center_time = time.time()
                elif not photo_taken and (time.time() - entered_center_time > 2):
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"capture_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Photo captured: {filename}")
                    show_feedback("📸 Photo Captured!", "lightgreen")
                    photo_taken = True
            else:
                entered_center_time = None
                photo_taken = False

    status_label.config(
        text="Blue Object Detected ✅" if blue_detected else "No Blue Object",
        foreground="green" if blue_detected else "red"
    )

    filtered = apply_filter(frame, current_filter)
    img = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    canvas.imgtk = imgtk
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
    root.after(10, update_frame)

def capture_photo():
    ret, frame = cap.read()
    if ret:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"manual_capture_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Manual photo captured: {filename}")
        show_feedback("📸 Manual Photo Captured!", "lightblue")

def change_filter(event):
    global current_filter
    current_filter = filter_menu.get()

# ---- TKINTER UI ----
root = tk.Tk()
root.title("Photobooth")
root.geometry("700x600")
root.configure(bg="#111")

canvas = tk.Canvas(root, width=640, height=480, bg="black", highlightthickness=0)
canvas.pack(pady=10)

status_label = tk.Label(root, text="No Blue Object", font=("Arial", 14), bg="#111", fg="red")
status_label.pack()

feedback_label = tk.Label(root, text="", font=("Arial", 14), bg="#111", fg="white")
feedback_label.pack()

filter_menu = ttk.Combobox(root, values=["None", "Grassau", "Average", "Gaussian", "Gradient"])
filter_menu.set("None")
filter_menu.bind("<<ComboboxSelected>>", change_filter)
filter_menu.pack(pady=5)

capture_btn = ttk.Button(root, text="📸 Capture", command=capture_photo)
capture_btn.pack(pady=10)

update_frame()
root.mainloop()
cap.release()
