import yaml
import argparse
import os
import logging
import boto3
from boto3.s3.transfer import S3Transfer
from youtube3 import YoutubeClient
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from youtube_dl.utils import sanitize_filename


def download_videos(youtube_client, playlist_id, playlist_key, video_output_path):

    playlist_output = os.path.join(video_output_path, playlist_key)
    for video_items in youtube_client.iterate_videos_in_playlist(playlist_id):
        for item in video_items['items']:
            snippet = item['snippet']
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            title = snippet['title']
            print(video_id, title)
            url = "http://www.youtube.com/watch?v=" + video_id

            with YoutubeDL({'format': str(video_format), 'merge-output-format': 'mp4', 'cachedir': False,
                            'outtmpl': playlist_output + '/' + DEFAULT_OUTTMPL, "nooverwrites": True, "restrictfilenames": True}) as youtube_dl:
                youtube_dl.download([url])
    return playlist_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist_id', type=str)
    with open('config.yml') as f:
        config = yaml.safe_load(f)
        output_path = config['output_dir']
        client_json_file = config['client_json_file']
        video_format = config['video_format']
        s3_bucket = config['s3_bucket']


    if not os.path.exists(output_path):
        os.makedirs(output_path)
    video_output_path = os.path.join(output_path, 'videos')
    if not os.path.exists(video_output_path):
        os.makedirs(video_output_path)

    args = parser.parse_args()
    playlist_id = args.playlist_id
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), client_json_file))
    playlist_name = youtube_client.playlist_name(playlist_id)
    logging.info("Processing channel: {}".format(playlist_name))
    playlist_key = playlist_id + '_' + sanitize_filename(playlist_name, restricted=True)
    playlist_output = os.path.join(video_output_path, playlist_key)
    download_videos(youtube_client=youtube_client, playlist_id=playlist_id, playlist_key=playlist_key, video_output_path=video_output_path)
    if s3_bucket:
        s3_client = boto3.client('s3')
        transfer = S3Transfer(s3_client)
    if s3_client:

        files = os.listdir(playlist_output)
        for file in files:
            full_file = os.path.join(playlist_output, file)
            dest_file = os.path.join('videos', playlist_key, file)
            logging.info("Transferring {} to {}:{}".format(full_file, s3_bucket, dest_file))
            transfer.upload_file(full_file, s3_bucket, dest_file)


