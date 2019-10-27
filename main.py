import yaml
import argparse
import os
import logging
from youtube3 import YoutubeClient
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from youtube_dl.utils import sanitize_filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist_id', type=str)
    with open('config.yml') as f:
        config = yaml.safe_load(f)
        output_path = config['output_dir']
        client_json_file = config['client_json_file']


    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_output_path = os.path.join(output_path, 'videos')
    if not os.path.exists(video_output_path):
        os.makedirs(video_output_path)
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), client_json_file))
    args = parser.parse_args()
    playlist_id = args.playlist_id
    playlist_name = youtube_client.playlist_name(playlist_id)
    logging.info("Processing channel: {}".format(playlist_name))
    for video_items in youtube_client.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            snippet = item['snippet']
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            title = snippet['title']
            print(video_id, title)
            url = "http://www.youtube.com/watch?v=" + video_id
            playlist_output = os.path.join(video_output_path, playlist_id + '_' + sanitize_filename(playlist_name))
            with YoutubeDL({'format': 'best', 'merge-output-format': 'mp4', 'cachedir': False,
                            'outtmpl': playlist_output + '/' + DEFAULT_OUTTMPL, "nooverwrites": True}) as youtube_dl:
                youtube_dl.download([url])

