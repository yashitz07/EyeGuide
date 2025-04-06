import cv2
import pytesseract
from gtts import gTTS
import os
from datetime import datetime
import platform
from flask import Flask

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/captured'
app.config['AUDIO_FOLDER'] = 'static/audio'

# Set tesseract path only for Windows
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def perform_ocr_and_audio(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_adjusted = adjust_brightness_contrast(img, alpha=1.5, beta=20)

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    adjusted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'adjusted_image_{timestamp}.jpg')
    cv2.imwrite(adjusted_image_path, cv2.cvtColor(img_adjusted, cv2.COLOR_RGB2BGR))

    text = pytesseract.image_to_string(img_adjusted)
    print("Extracted Text:")
    print(text)

    if text.strip():
        audio_file = os.path.join(app.config['AUDIO_FOLDER'], f'output_{timestamp}.mp3')
        tts = gTTS(text=text, lang='en')
        tts.save(audio_file)
        return text, audio_file, adjusted_image_path, timestamp
    else:
        return "Error: No text detected in uploaded image", "", "", ""
