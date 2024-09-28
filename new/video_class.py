from pytube import YouTube


class Video():
    def __init__(self, url: str):
        self.url = url
        self.yt_object = YouTube(url)
