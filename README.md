Models in music/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=80, unique=True)

class Song(models.Model):
    title = models.CharField(max_length=120)
    artist = models.CharField(max_length=120)

class Playlist(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)

Views in music/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User, Song, Playlist

def add_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        song = Song.objects.create(title=title, artist=artist)
        return JsonResponse({'message': 'Song added successfully'}, status=201)

def create_playlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user, created = User.objects.get_or_create(username="default_user")
        playlist = Playlist.objects.create(name=name, user=user)
        return JsonResponse({'message': 'Playlist created successfully'}, status=201)

def add_song_to_playlist(request):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        song_id = request.POST.get('song_id')
        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)
        playlist.songs.add(song)
        return JsonResponse({'message': 'Song added to playlist successfully'}, status=200)

URL Configuration in music/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_song/', views.add_song, name='add_song'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('add_song_to_playlist/', views.add_song_to_playlist, name='add_song_to_playlist'),
]

Include URLs in SongScripts/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('music.urls')),
]

Template in music/templates/music/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music App</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
    <h1>Music App</h1>
    
    <!-- Add Song Form -->
    <form id="songForm">
        <input type="text" id="songTitle" placeholder="Song Title" required>
        <input type="text" id="songArtist" placeholder="Artist" required>
        <button type="submit">Add Song</button>
    </form>
    <!-- Create Playlist Form -->
    <form id="playlistForm">
        <input type="text" id="playlistName" placeholder="Playlist Name" required>
        <button type="submit">Create Playlist</button>
    </form>
    <script>
        document.getElementById('songForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const title = document.getElementById('songTitle').value;
            const artist = document.getElementById('songArtist').value;
            axios.post('/add_song/', { title, artist })
                .then(response => alert(response.data.message))
                .catch(error => console.error(error));
        });
        document.getElementById('playlistForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('playlistName').value;
            axios.post('/create_playlist/', { name })
                .then(response => alert(response.data.message))
                .catch(error => console.error(error));
        });
    </script>
</body>
</html>
