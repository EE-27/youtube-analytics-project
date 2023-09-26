import json
import os
import datetime

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate
class PlayList:

    api_key: str = os.getenv('API_YT')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id


        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.playlist_videos = playlist_videos

        json_load_from_api = json.dumps(self.playlist_videos, indent=2, ensure_ascii=False)
        plvideo_data = json.loads(json_load_from_api)
        self.plvideo_data = plvideo_data

        self.video_id = self.plvideo_data['items'][0]['contentDetails']['videoId']

        self.video_response = PlayList.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        json_load_from_api = json.dumps(self.video_response, indent=2, ensure_ascii=False)
        video_data = json.loads(json_load_from_api)
        self.video_data = video_data
        self.channel_id = self.video_data['items'][0]['snippet']['channelId']

        #

        playlists = PlayList.youtube.playlists().list(channelId=self.channel_id,  # title
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        json_load_from_api = json.dumps(playlists, indent=2, ensure_ascii=False)
        playlist_data = json.loads(json_load_from_api)

        for playlist in playlist_data['items']:
            if playlist['id'] == 'PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw':
                playlist_title = playlist['snippet']['title']
                break

        self.title = playlist_title  # title

        #

        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
    @property
    def total_duration(self):

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        json_load_from_api = json.dumps(video_response, indent=2, ensure_ascii=False)
        playlist_data = json.loads(json_load_from_api)
        self.playlist_data = playlist_data

        durations = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            seconds = duration.seconds % 60
            formatted_duration = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            durations.append(formatted_duration)

        hh = []
        mm = []
        ss = []

        for tm in durations:
            x = tm.split(":")
            hh.append(int(x[0]))
            mm.append(int(x[1]))
            ss.append(int(x[2]))


        time = datetime.timedelta(hours=sum(hh), minutes=sum(mm), seconds=sum(ss))

        self.total_duration = time
        self.time = time
        return self.time

    def __str__(self):
        return self.total_duration

    @total_duration.setter
    def total_duration(self, value):
        self.time = value
        return value


    def show_best_video(self):
        sorted_videos = sorted(self.playlist_data['items'], key=lambda x: int(x['statistics']['likeCount']), reverse=True)
        best = sorted_videos[0]["id"]
        return f"https://youtu.be/{best}"


# pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
# pl.show_best_video()