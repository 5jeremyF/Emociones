# Generated by Django 4.2.8 on 2024-06-25 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='nombre')),
                ('description', models.CharField(max_length=200, verbose_name='descripcion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('song_path', models.CharField(max_length=150, verbose_name='direccion')),
                ('title', models.CharField(max_length=100, verbose_name='nombre')),
                ('artist', models.CharField(max_length=100, verbose_name='artista')),
                ('genre', models.CharField(max_length=50, verbose_name='género')),
                ('link', models.CharField(max_length=150, verbose_name='enlace')),
                ('preview', models.CharField(max_length=150, verbose_name='enlace')),
                ('duration', models.CharField(max_length=150, verbose_name='duracion')),
                ('image', models.ImageField(blank=True, max_length=500, null=True, upload_to='Musica', verbose_name='Foto')),
                ('emotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.emotion')),
            ],
            options={
                'unique_together': {('title', 'emotion')},
            },
        ),
        migrations.CreateModel(
            name='HistoriesMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Music.music')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
