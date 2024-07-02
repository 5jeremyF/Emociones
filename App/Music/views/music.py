from ..models import Music
from App.core.models import Emotion
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
import json

from App.security.mixins.mixim import PermissionMixim

class MusicCreateViews(CreateView):
    model = Music
    fields = ['emotion', 'title', 'artist', 'genre', 'link', 'preview', 'duration', 'image']

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            emotion_name = data.get('emotion')
            emotion, created = Emotion.objects.get_or_create(name=emotion_name)

            # Intentar crear una nueva instancia de Music
            try:
                music = Music.objects.create(
                    emotion=emotion,
                    title=data.get('title'),
                    song_path=data.get('song_path'),
                    artist=data.get('artist'),
                    link=data.get('link'),
                    preview=data.get('preview'),
                    duration=data.get('duration'),
                    image=data.get('image')
                )
                return JsonResponse({'status': 'success', 'message': 'Music saved successfully'})
            except IntegrityError:
                # Si ya existe, buscar la instancia existente
                music = Music.objects.get(emotion=emotion, title=data.get('title'))
                return JsonResponse({'status': 'exists', 'message': 'Music already exists', 'music_id': music.id})

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")