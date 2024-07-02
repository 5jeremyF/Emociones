import json

from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView
from django.http import JsonResponse, HttpResponseBadRequest
from ..models import Favorities, Music

from App.security.mixins.mixim import PermissionMixim
from ...security.models import User


class AddToFavoritiesView(PermissionMixim,View):
    def post(self, request):
        data = request.body
        print(data)
        try:
            data = json.loads(request.body)
            music_id = data.get('music_id')
            print(music_id)
            user_id = request.user.id
            print(user_id)
            if not music_id:
                return HttpResponseBadRequest('Music ID is required')

            # Obtener la música correspondiente
            music = get_object_or_404(Music, title=music_id)
            user = get_object_or_404(User, id=user_id)
            print(music)
            # Crear o actualizar el favorito del usuario
            favorite, created = Favorities.objects.get_or_create(user=user, music=music)
            print(favorite)

            return JsonResponse({'success': True,'music': music.title})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class FavoritiesListView(PermissionMixim,ListView):
    model = Favorities
    template_name = 'favorities/list.html'
    context_object_name = 'favorities'

    def get_queryset(self):
        user = self.request.user
        return Favorities.objects.filter(user=user)