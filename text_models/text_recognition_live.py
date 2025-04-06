import cv2
import pytesseract
import numpy as np
import pyttsx3
import time
import platform

# Set tesseract path only if on Windows
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_text(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return pytesseract.image_to_string(thresh)

def perform_live_text():
    engine = pyttsx3.init()
    cap = cv2.VideoCapture(0)

    last_speech_time = 0
    speech_gap = 2  # seconds

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detected_text = detect_text(frame)

        h, w, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (w, 30), (0, 0, 0), -1)
        cv2.putText(frame, detected_text.strip(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        current_time = time.time()

        if detected_text.strip() and (current_time - last_speech_time) > speech_gap:
            engine.say(detected_text)
            engine.runAndWait()
            last_speech_time = current_time

        cv2.imshow('Live OCR - Press "c" to stop', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cap.release()
    cv2.destroyAllWindows()
