import youtube_dl
import urllib.request
import urllib.parse
import re
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def download_song(url: str, playlist: str, file_name = None):

    try:
        directory = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(os.path.join(directory, "playlists", playlist)):
            os.mkdir(os.path.join(directory, "playlists", playlist))

        save_dir = os.path.join(directory, "playlists", playlist)

        if file_name is None:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl" : f"{save_dir}/%(title)s.%(ext)s",
                "postprocessor_args": ["-loglevel", "panic"],
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
        
        else:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl" : f"{save_dir}/{file_name}.%(ext)s",
                "postprocessor_args": ["-loglevel", "panic"],
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except:
        return False

def get_song_url(song: str):

    try:
        song = urllib.parse.quote(song)
        html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + song)
        search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
        url = "https://youtube.com/watch?v=" + search_results[0]

        return url

    except:
        return False

def check_url(content: str):

    try:
        regex = r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$"
        url = re.findall(regex, content)

        if url:
            return True
        
        else:
            return False

    except:
        return False

"""
DevPlayer
Devansh Singh, 2021
"""
