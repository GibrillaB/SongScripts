from django.shortcuts import render
from django.conf import settings
import requests
from urllib.parse import urlencode
from .models import Query

def home(request):
    return render(request, "home.html")


def search_lyrics(request):
    query = request.GET.get('query', '')  # Get the search term from user input
    search_results = None
    


    if query:
        #Save query to database
        Query.objects.create(query_text=query)
        # API call to Genius to search for lyrics
        genius_url = f"https://api.genius.com/search?q={query}"
        headers = {'Authorization': f'Bearer {settings.GENIUS_ACCESS_TOKEN}'}
        response = requests.get(genius_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            search_results = data.get('response', {}).get('hits', [])
    #Retrieve the most recent queries
    recent_queries = Query.objects.order_by('-timestamp')[:10]
    
    return render(request, 'search.html', {'query': query, 'search_results': search_results, 'recent_queries': recent_queries,})