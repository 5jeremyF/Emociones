import base64
import cv2
import numpy as np
import os
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from ..constants.Emotion import EMOTION
from App.Music.models import Music

from App.security.mixins.mixim import PermissionMixim

logger = logging.getLogger(__name__)

class EmotionCaptureView(PermissionMixim, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.faceNet = cv2.dnn.readNet(
            os.path.join(settings.BASE_DIR, 'App\\ReconocimientoDemociones\\utils\\modelos\\deploy.prototxt'),
            os.path.join(settings.BASE_DIR, 'App\\ReconocimientoDemociones\\utils\\modelos\\res10_300x300_ssd_iter_140000.caffemodel')
        )
        self.emotionModel = load_model(os.path.join(settings.BASE_DIR, 'App\\ReconocimientoDemociones\\utils\\modelos\\modelFEC.h5'))
        self.classes = EMOTION
        self.is_processing = False 

    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Necesitas autenticarte para acceder a esta función.'}, status=403)
            if self.is_processing:
                return JsonResponse({'error': 'Procesando imagen anterior, espera un momento'}, status=400)

            self.is_processing = True

            data = json.loads(request.body.decode('utf-8'))
            image_data = data.get('image', None)

            if not image_data:
                return JsonResponse({'error': 'No se encontraron datos de imagen'}, status=400)

            encoded_image = image_data.split(',')[1]
            image_data = base64.b64decode(encoded_image)
            image = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            (locs, preds) = self.predict_emotions(image)

            emotions_data = []
            for (box, pred) in zip(locs, preds):
                (Xi, Yi, Xf, Yf) = box
                emotion = self.classes[np.argmax(pred)]
                confidence = max(pred) * 100
                emotions_data.append({
                    'emotion': emotion,
                    'confidence': float(confidence)
                })

            main_emotion = emotions_data[0]['emotion']
            songs_list = self.get_songs_by_emotion(main_emotion)

            self.is_processing = False

            return JsonResponse({'emotions': emotions_data, 'songs': songs_list}, status=200)

        except IndexError as ie:
            logger.error(f'Error de índice al procesar la imagen: {str(ie)}')
            self.is_processing = False
            return JsonResponse({'error': 'Error de índice al procesar la imagen'}, status=500)

        except Exception as e:
            logger.error(f'Error procesando la imagen: {str(e)}')
            self.is_processing = False
            return JsonResponse({'error': str(e)}, status=500)

    def predict_emotions(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()

        faces = []
        locs = []
        preds = []

        for i in range(0, detections.shape[2]):
            if detections[0, 0, i, 2] > 0.4:
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (Xi, Yi, Xf, Yf) = box.astype("int")

                if Xi < 0: Xi = 0
                if Yi < 0: Yi = 0

                face = frame[Yi:Yf, Xi:Xf]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)

                preds.append(self.emotionModel.predict(face, verbose=0)[0])
                locs.append((Xi, Yi, Xf, Yf))
        if not locs:
            return [], []

        return (locs, preds)

    def get_songs_by_emotion(self, emotion):
        base_dir = os.path.join(settings.STATIC_ROOT, emotion)
        songs = os.listdir(base_dir)
        songs_list = [f'{settings.STATIC_URL}{emotion}/{song}' for song in songs]
        logger.debug(f'Songs list: {songs_list}')
        return songs_list
