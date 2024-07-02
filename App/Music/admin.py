from django.contrib import admin
from .models import Music, HistoriesMusic,Favorities
# Register your models here.
@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'emotion', 'duration']
    list_filter = ['artist', 'emotion', 'genre']
    search_fields = ['title', 'artist', 'emotion']
    
@admin.register(Favorities)

class FavoritiesAdmin(admin.ModelAdmin):
    list_display = ['user', 'music']
    search_fields = ['music__title']
    
@admin.register(HistoriesMusic)

class HistoriesMusicAdmin(admin.ModelAdmin):
    list_display = ['user', 'music']
    list_filter = ['user']  
    search_fields = ['music__title']
