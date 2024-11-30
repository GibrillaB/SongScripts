from django.shortcuts import render
from django.conf import settings
import requests
from urllib.parse import urlencode

def home(request):
    return render(request, "home.html")

def search_lyrics(request):
    query = request.GET.get('query', '')  # Get the search term from user input
    search_results = None

    if query:
        # API call to Genius to search for lyrics
        genius_url = f"https://api.genius.com/search?q={query}"
        headers = {'Authorization': f'Bearer {settings.GENIUS_ACCESS_TOKEN}'}
        response = requests.get(genius_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            search_results = data.get('response', {}).get('hits', [])

    return render(request, 'search.html', {'query': query, 'search_results': search_results})