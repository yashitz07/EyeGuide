from gtts import gTTS
import torch
from PIL import Image
import os
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config['AUDIO_FOLDER'] = 'static/audio'

def detect_objects(image_path):
    # Set GitHub token for torch.hub to avoid rate limiting
    token = os.getenv('GITHUB_TOKEN')
    if token:
        os.environ['GITHUB_TOKEN'] = token

    # Load the YOLOv5 model with token-based access
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)
    
    # Load an image
    img = Image.open(image_path)
    
    # Inference
    results = model(img)
    
    # Get detected objects
    detected_objects = results.pandas().xyxy[0]['name'].unique()
    
    if detected_objects.size > 0:
        objects_list = ", ".join(detected_objects)
        description_text = f"The objects detected in the image are: {objects_list}."
    else:
        description_text = "No objects detected."
    
    # Generate audio from text
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    tts = gTTS(description_text, lang='en')
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], f'desciption_{timestamp}.mp3')
    tts.save(audio_path)
    
    return description_text, audio_path, timestamp
