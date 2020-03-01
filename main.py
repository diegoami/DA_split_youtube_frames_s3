import yaml
import argparse
import os
import logging
import sys
from youtube3 import YoutubeClient
from youtube_dl.utils import sanitize_filename

from split_youtube_frames.youtube_downloader import download_videos
from split_youtube_frames.s3_uploader import upload_videos_to_s3, upload_frames_to_s3
from split_youtube_frames.frame_splitter import split_into_frames

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('command', help='Subcommand to run')
    # parse_args defaults to [1:] for args, but you need to
    # exclude the rest of the args too, or validation will fail
    args = parser.parse_args(sys.argv[1:2])
    if args.command not in ['download_videos', 'upload_videos_to_s3', 'upload_frames_to_s3', 'split_into_frames', 'do_local', 'do_s3']:
        print
        'Unrecognized command'
        parser.print_help()
        exit(1)
    # use dispatch pattern to invoke method with same name

    with open('config.yml') as f:
        config = yaml.safe_load(f)
    if not os.path.exists(config['output_path']):
        os.makedirs(config['output_path'])
    video_output_path = os.path.join(config['output_path'], 'videos')
    frame_output_path = os.path.join(config['output_path'], 'frames')
    if not os.path.exists(video_output_path):
        os.makedirs(video_output_path)

    args = parser.parse_args()
    playlist_id = config['playlist_id']
    video_range_keep = config['video_range_keep']
    video_range_train = config['video_range_train']
    video_range_test = config['video_range_test']
    youtube_client = YoutubeClient(config['client_json_file'])
    playlist_name = youtube_client.playlist_name(playlist_id)

    playlist_key = playlist_id + '_' + sanitize_filename(playlist_name, restricted=True)
    playlist_output= os.path.join(video_output_path, playlist_key)
    frame_output = os.path.join(frame_output_path,  playlist_key)

    if args.command in ['download_videos', 'do_local', 'do_s3']:
        download_videos(youtube_client=youtube_client, playlist_id=playlist_id, playlist_key=playlist_key,  video_output_path=video_output_path, video_format=config['video_format'], video_range_keep= video_range_keep, video_range_train=video_range_train, video_range_test=video_range_test)
    if args.command in ['upload_videos_to_s3', 'do_s3']:
        upload_videos_to_s3(s3_bucket=config['s3_bucket'], playlist_output=playlist_output, playlist_key=playlist_key)
    if args.command in ['split_into_frames', 'do_local', 'do_s3']:
        split_into_frames(frame_output=frame_output, playlist_output=playlist_output, frame_interval=config['frame_interval'], video_range_train=video_range_train, video_range_test=video_range_test)
    if args.command in ['upload_frames_to_s3', 'do_s3']:
        upload_frames_to_s3(s3_bucket=config['s3_bucket'], frame_output=frame_output, frame_key=playlist_key)