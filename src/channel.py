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

    def print_info(self) -> None:
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

