import logging
import os
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL


def download_videos(youtube_client, playlist_id, playlist_key, video_output_path, video_format):
    playlist_output = os.path.join(video_output_path, playlist_key)
    logging.info("Downloading from playlist {} to {}".format(playlist_key, playlist_output))

    for video_items in youtube_client.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            snippet = item['snippet']
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            title = snippet['title']
            print(video_id, title)
            video_info = youtube_client.get_video(video_id)
            url = "http://www.youtube.com/watch?v={}".format(video_id)

            with YoutubeDL({'format': str(video_format), 'merge-output-format': 'mp4', 'cachedir': False,
                            'outtmpl': playlist_output + '/' + DEFAULT_OUTTMPL, "nooverwrites": True, "restrictfilenames": True}) as youtube_dl:
                youtube_dl.download([url])
    return playlist_output
