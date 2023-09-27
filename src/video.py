import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# import isodate
class Video:
    api_key: str = os.getenv('API_YT')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id

        video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_response = video_response

        json_load_from_api = json.dumps(self.video_response, indent=2, ensure_ascii=False)
        video_data = json.loads(json_load_from_api)
        self.video_data = video_data

        #attributes
        try:
            self.title = self.video_data['items'][0]['snippet']['title']
            self.video_url = self.video_data['items'][0]['snippet']['thumbnails']['default']['url']
            self.view_count = self.video_data['items'][0]['statistics']['viewCount']
            self.like_count = self.video_data['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None


    def __str__(self):
        return self.video_data['items'][0]['snippet']['title']

class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

        playlist_videos = PLVideo.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        self.playlist_videos = playlist_videos


    def __str__(self):
        return self.video_data['items'][0]['snippet']['title']

#  pl = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
