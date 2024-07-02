from django.db import models
from ..core.models import ModelBase, Emotion
from ..security.models import User
from django.utils import timezone

# Create your models here.
#class MusicManager(models.Manager):
 #   def by_emotion(self, emotion):
  #      return self.filter(emotion__name=emotion)
class Music(ModelBase):
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    song_path = models.CharField("direccion", max_length=150)
    title = models.CharField("nombre", max_length=100)
    artist = models.CharField("artista", max_length=100)
    genre = models.CharField("género", max_length=50)
    link = models.CharField("enlace", max_length=150)
    preview = models.CharField("enlace", max_length=150)
    duration = models.CharField("duracion", max_length=150)
    image = models.ImageField(
        verbose_name='Foto',
        upload_to='Musica',
        max_length=500,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('title', 'emotion')

    def __str__(self):
        return f"{self.title}- {self.artist}"

    #objects = models.Manager()  # Manager predeterminado
    #custom_manager = MusicManager()  # Manager personalizado


class PlayList(ModelBase):
    name = models.CharField("nombre",max_length=100)
    description = models.CharField("descripcion",max_length=200)

class HistoriesMusic(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    #objects = models.Manager()
    #custom_manager = MusicManager()
    def __str__(self):
        return f"{self.music.title}-{self.music.emotion.name}"

class Favorities(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.music.title}-{self.music.emotion.name} - {self.user.username}"