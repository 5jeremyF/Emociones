from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.http import JsonResponse
from datetime import date
from ..models import HistoriesMusic, Music
from App.security.models import User
import json
from django.utils import timezone
from App.Music.models import Music, HistoriesMusic
from App.security.mixins.mixim import PermissionMixim

class AddToHistoryView(PermissionMixim,View):
    def post(self, request):
        data = json.loads(request.body)
        title = data.get('music_id')
        user_id = request.user.id
        print(data,user_id,title)

        # Verificar si la música con el título existe en la base de datos
        music = get_object_or_404(Music, title=title)
        print(music)
        user = get_object_or_404(User, id=user_id)

        # Crear una nueva entrada en el historial
        history = HistoriesMusic.objects.create(user=user, music=music, date=timezone.now())

        return JsonResponse({'success': True})
class HistoryListView(PermissionMixim,ListView):
    model = HistoriesMusic
    template_name = 'histories/list.html'
    context_object_name = 'histories'

    def get_queryset(self):
        user = self.request.user
        return HistoriesMusic.objects.filter(user=user)

