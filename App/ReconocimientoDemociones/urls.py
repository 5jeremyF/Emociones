from django.urls import path

from ..ReconocimientoDemociones.views.emocion import EmotionCaptureView

urlpatterns = [
    path('detect_emotion', EmotionCaptureView.as_view(), name='detect_emotion'),
]