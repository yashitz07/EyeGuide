import cv2
import torch
import time
import os

if os.environ.get("RENDER") != "true":
    import pyttsx3

def object_detection():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
    tts_engine = pyttsx3.init() if os.environ.get("RENDER") != "true" else None

    def generate_scene_description(objects):
        return ' and '.join(objects) + ' are visible in the scene.'

    cap = cv2.VideoCapture(0)
    last_speech_time = time.time() - 6

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detected_objects = [model.names[int(x)] for x in results.xyxy[0][:, -1]]

        if detected_objects and (time.time() - last_speech_time) >= 6:
            last_speech_time = time.time()
            scene_description = generate_scene_description(detected_objects)
            print(scene_description)
            if tts_engine:
                tts_engine.say(scene_description)
                tts_engine.runAndWait()

        cv2.imshow('press c to stop detection.', results.render()[0])
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_objects
