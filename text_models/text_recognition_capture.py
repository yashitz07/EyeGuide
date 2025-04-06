import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime
import platform

# Set tesseract path only for Windows
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def perform_text_capture():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            orig_path = os.path.join('static', 'captured', 'original_image.jpg')
            adj_path = os.path.join('static', 'captured', 'adjusted_image.jpg')
            cv2.imwrite(orig_path, frame)

            adjusted_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=20)
            cv2.imwrite(adj_path, adjusted_frame)

            cap.release()
            cv2.destroyAllWindows()
            break

        elif key == 27:
            cap.release()
            cv2.destroyAllWindows()
            return "Capture cancelled", "", "", ""

    img_path = os.path.join('static', 'captured', 'adjusted_image.jpg')
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        text_output = pytesseract.image_to_string(img)

        if text_output.strip():
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            audio_path = os.path.join('static', 'audio', f"output_audio_{timestamp}.mp3")

            tts = gTTS(text=text_output, lang='en')
            tts.save(audio_path)

            return text_output, img_path, audio_path, timestamp
        else:
            return "Error: No text detected in the captured image", "", "", ""
    else:
        return "Error: Adjusted image not found", "", "", ""
