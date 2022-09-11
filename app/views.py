from turtle import title
from django.shortcuts import render, HttpResponse
from django.conf import settings
import requests
from isodate import parse_duration
from .models import videos


def index(request):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    params1 = {
        'part': 'snippet',
        'q': ' Eminem ',
        'key': settings.YOUTUBE_DATA_API_SEARCH_KEY,
        'maxResults': 9,
        'type': 'video'
    }

    video_ids = []

    r = requests.get(search_url, params=params1)
    results = r.json()['items']

    for result in results:
        video_ids.append(result['id']['videoId'])

    params2 = {
        'key': settings.YOUTUBE_DATA_API_SEARCH_KEY,
        'part': 'snippet,contentDetails',
        'id': ','.join(video_ids),
        'maxResults': 9,

    }

    r = requests.get(video_url, params=params2)
    results = r.json()['items']

    videos = []
    for result in results:
        video_data = {
            'title': result['snippet']['title'],
            'id': result['id'],
            'url': f'https://www.youtube.com/watch?v={result["id"]}',
            'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail': result['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'webpage/index.html', context)


def search(request):
    # if(request.method=='get'):
        query = request.GET['query']
        allvid = videos.objects.filter(name__icontains=query)
        params = {'allvid': allvid}
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        params1 = {'allvid': allvid,
        'part': 'snippet',
        'q': ' query ',
        'key': settings.YOUTUBE_DATA_API_SEARCH_KEY,
        'maxResults': 9,
        'type': 'video'
    }

        video_ids = []

        r = requests.get(search_url, params=params1)
        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])

        params2 = {
        'key': settings.YOUTUBE_DATA_API_SEARCH_KEY,
        'part': 'snippet,contentDetails',
        'id': ','.join(video_ids),
        'maxResults': 9,

    }

        r = requests.get(video_url, params=params2)
        results = r.json()['items']

        vid = []
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail':result['snippet']['thumbnails']['high']['url']
            }
            vid.append(video_data)

        context={
            'videos': vid
        }

        return render(request,'webpage/search.html',params)