from pytubefix import YouTube
from pytubefix.cli import on_progress
 
url = "https://www.youtube.com/watch?v=8oYU4dkS0AY"
 
yt = YouTube(url, 'WEB_CREATOR')
print(yt.title)
 
ys = yt.streams.get_highest_resolution()
ys.download()