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

# Create your views here.
def Home(request):
    return render(request, 'home.html')


class FavoriteView(PermissionMixim, View):
    template_name='favorities/list.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class HistoryView(PermissionMixim, View):
    template_name='histories/list.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        
class PlaylistView(View):
    template_name='playlist/list.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def deezer_search(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    url = f'https://api.deezer.com/search?q={query}'
    response = requests.get(url)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to fetch data from Deezer'}, status=response.status_code)



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
