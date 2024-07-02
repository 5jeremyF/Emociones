from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import base64
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import random
import os
from django.conf import settings

EMOTION = ['angry', 'happy', 'sad', 'neutral', 'surprise', 'fear', 'disgust']

class EmotionCaptureView(View):
    template_name = 'your_template_name.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        image_data = request.POST.get('image')
        emotion = self.detect_emotion(image_data)
        song_path = self.select_song(emotion)
        return JsonResponse({'emotion': emotion, 'song_path': song_path})

    def detect_emotion(self, image_data):
        # Decodificar la imagen desde base64
        image_data = base64.b64decode(image_data.split(',')[1])
        image = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Procesar la imagen y predecir la emoción
        face_net = cv2.dnn.readNet('App/ReconocimientoDemociones/utils/modelos/deploy.prototxt', 'App/ReconocimientoDemociones/utils/modelos/res10_300x300_ssd_iter_140000.caffemodel')
        emotion_model = load_model('App/ReconocimientoDemociones/utils/modelos/modelFEC.h5')
        blob = cv2.dnn.blobFromImage(image, 1.0, (224, 224), (104.0, 177.0, 123.0))

        face_net.setInput(blob)
        detections = face_net.forward()

        for i in range(detections.shape[2]):
            if detections[0, 0, i, 2] > 0.4:
                box = detections[0, 0, i, 3:7] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
                (Xi, Yi, Xf, Yf) = box.astype('int')
                face = image[Yi:Yf, Xi:Xf]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)

                preds = emotion_model.predict(face)
                emotion = EMOTION[np.argmax(preds[0])]
                return emotion

        return random.choice(EMOTION)  # Fallback si no se detecta ninguna cara

    def select_song(self, emotion):
        base_dir = os.path.join(settings.STATIC_ROOT, emotion)
        songs = os.listdir(base_dir)
        song = random.choice(songs)
        return f'{settings.STATIC_URL}{emotion}/{song}'
