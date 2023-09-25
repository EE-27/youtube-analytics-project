import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# import isodate
class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        api_key: str = os.getenv('API_YT')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_response = video_response

        json_load_from_api = json.dumps(self.video_response, indent=2, ensure_ascii=False)
        video_data = json.loads(json_load_from_api)
        self.video_data = video_data

    def __str__(self):
        return self.video_data['items'][0]['snippet']['title']

class PLVideo:

    def __init__(self, video_id, playlist_id):
        self.video_id = video_id
        self.playlist_id = playlist_id
        api_key: str = os.getenv('API_YT')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.video_response = video_response

        json_load_from_api = json.dumps(self.video_response, indent=2, ensure_ascii=False)
        video_data = json.loads(json_load_from_api)
        self.video_data = video_data

        self.playlist_videos = playlist_videos

        json_load_from_api = json.dumps(self.playlist_videos, indent=2, ensure_ascii=False)
        plvideo_data = json.loads(json_load_from_api)
        self.plvideo_data = plvideo_data
        print(self.video_data)
        print(self.plvideo_data)

    def __str__(self):
        return self.video_data['items'][0]['snippet']['title']

pl = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
