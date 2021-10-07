from django.shortcuts import render
from django.http import HttpResponse
from .forms import DownloadForm
import youtube_dl
import re

def download_video(request):
    global context
    form = DownloadForm(request.POST or None)
    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        
        if not re.match(regex, video_url):
            return HttpResponse("Enter Correct URL")

        if 'm.' in video_url:
            video_url = video_url.replace(u'm.', u'')

        elif 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
            video_url = 'https://www.youtube.com/watch?v=' + video_id

        if len(video_url.split("=")[-1]) < 11:
            return HttpResponse("Enter Correct URL")

        ydl_options = {}
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            meta_data = ydl.extract_info(video_url, download=False)
        
        video_audio_streams = []
        for data in meta_data['formats']:
            file_size = data['filesize']
            if file_size is not None:
                file_size = f"{round(int(file_size) / 1000000, 2)} MB"
            
            resolution = 'Audio'
            if data['height'] is not None:
                resolution = f"{data['height']}x{data['width']}"
            video_audio_streams.append({
                "resolution":resolution,
                "extension": data['ext'],
                "file_size": file_size,
                "video_url": data['url'],
            })
        video_audio_streams = video_audio_streams[::-1]
        context = {
            "form": form,
            "title": meta_data['title'],
            "channel": meta_data['channel'],
            "streams": video_audio_streams,
            "likes": meta_data['like_count'],
            "dislikes": meta_data['dislike_count'],
            "thumbnail": meta_data['thumbnails'][3]['url'],
            "duration": f"{round(int(meta_data['duration'])/60, 1)} Minutes",
            "views": f"{int(meta_data['view_count'])}",
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html', {"form": form})
                


