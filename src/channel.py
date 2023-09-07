import json
import os

# pip install google-api-python-client
from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        api_key: str = os.getenv('API_YT')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.channel = channel

        json_load_from_api = json.dumps(self.channel, indent=2, ensure_ascii=False)
        yt_data = json.loads(json_load_from_api)

        # tested by homework-2/main.py
        self.title = yt_data["items"][0]["snippet"]["title"]
        self.video_count = yt_data["items"][0]["statistics"]["videoCount"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"

        # not tested
        self.description = yt_data["items"][0]["snippet"]["description"]
        self.subscriberCount = yt_data["items"][0]["statistics"]["subscriberCount"]
        self.videoCount = yt_data["items"][0]["statistics"]["videoCount"]
        self.viewCount = yt_data["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls, api_key=None):
        if api_key is None:
            api_key = os.getenv('API_YT')

        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def to_json(self, file_name):
        json_load_from_api = json.dumps(self.channel, indent=2, ensure_ascii=False)
        yt_data = json.loads(json_load_from_api)

        with open(file_name, "w") as json_file:
            json.dump(yt_data, json_file)
