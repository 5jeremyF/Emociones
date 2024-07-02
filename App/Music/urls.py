from django.urls import path

from App.Music.views import emotionCapture, HistroriesByMusic, music
from App.Music.views.favoritiesView import AddToFavoritiesView, FavoritiesListView
from App.Music.views.music import MusicCreateViews
from App.Music.views.views import FavoriteView, HistoryView, PlaylistView, deezer_search

urlpatterns = [
    path('', emotionCapture.EmotionCaptureView.as_view(), name='detectEmotionBtn'),
    path('savemusic',music.MusicCreateViews.as_view(), name='saveMusic'),
    path('saveHistories',HistroriesByMusic.AddToHistoryView.as_view(), name='saveMusic'),
    path('histories', HistroriesByMusic.HistoryListView.as_view(), name='history'),
    path('favorities', FavoritiesListView.as_view(), name='favorities'),
    path('add_to_favorites', AddToFavoritiesView.as_view(), name='add_to_favorites'),

    path('deezer_search/', deezer_search, name='deezer_search'),

]
