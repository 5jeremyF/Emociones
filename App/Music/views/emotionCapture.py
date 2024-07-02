from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import os
import logging
import random
import requests
from django.http import JsonResponse
from App.security.mixins.mixim import PermissionMixim

EMOTION = ['angry', 'happy', 'sad', 'neutral', 'surprise', 'fear', 'disgust']

logger = logging.getLogger(__name__)

class EmotionCaptureView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        emotion = self.get_emotion()
        song_path = self.select_song(emotion)
        logger.debug(f'Song path: {song_path}')
        return JsonResponse({'emotion': emotion, 'song_path': song_path})

    def get_emotion(self):
        emotion = random.choice(EMOTION)
        return emotion

    def select_song(self, emotion):
        base_dir = os.path.join(settings.STATIC_ROOT, emotion)
        songs = os.listdir(base_dir)
        song = random.choice(songs)
        song_path = f'{settings.STATIC_URL}{emotion}/{song}'
        logger.debug(f'Full song path: {os.path.join(base_dir, song)}')
        return song_path
