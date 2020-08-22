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

    parser.add_argument('command', help='Subcommand to run', default='download_videos')
    parser.add_argument('configuration', help='configuration to run', default='config')

    args = parser.parse_args(sys.argv[1:3])
    if args.command not in ['download_videos', 'upload_videos_to_s3', 'upload_frames_to_s3', 'split_into_frames', 'do_local', 'do_s3']:
        print('Unrecognized command')
        parser.print_help()
        exit(1)
    # use dispatch pattern to invoke method with same name
    configuration_file = f'{args.configuration}.yml'
    if not os.path.exists(configuration_file):
        print(f'{configuration_file} does not exist')
        exit(1)

    with open(configuration_file) as f:
        config = yaml.safe_load(f)
    if not os.path.exists(config['output_path']):
        os.makedirs(config['output_path'])



    args = parser.parse_args()
    playlist_id = config.get('playlist_id', None)
    playlist_ids = config.get('playlist_ids', None)
    only_metadata = config.get('only_metadata', None)

    video_range_keep = config.get('video_range_keep', None)
    video_range_train = config.get('video_range_train', None)
    video_range_test = config.get('video_range_test', None)
    target_directory = config.get('target_directory', None)
    youtube_client = YoutubeClient(config['client_json_file'])
    if playlist_id:
        playlist_names = [youtube_client.playlist_name(playlist_id)]
    else:
        playlist_names = [youtube_client.playlist_name(playlist_id) for playlist_id in playlist_ids]

    target_key = target_directory + '_' + sanitize_filename(target_directory, restricted=True)
    output_path = config.get('output_path', '.')
    video_output_path = os.path.join(output_path, target_directory, 'videos')
    frame_output_path = os.path.join(output_path, target_directory, 'frames')
    metadata_output_path = os.path.join(output_path, target_directory, 'metadata')
    if not os.path.exists(video_output_path):
        os.makedirs(video_output_path)
    if not os.path.exists(metadata_output_path):
        os.makedirs(metadata_output_path)
    if not os.path.exists(frame_output_path):
        os.makedirs(frame_output_path)

    if args.command in ['download_videos', 'do_local', 'do_s3']:
        download_videos(youtube_client=youtube_client, playlist_ids=playlist_ids,   video_output_path=video_output_path, metadata_output_path=metadata_output_path, video_format=config['video_format'], video_range_keep= video_range_keep, video_range_train=video_range_train, video_range_test=video_range_test, only_metadata=only_metadata)
    if args.command in ['upload_videos_to_s3', 'do_s3']:
        upload_videos_to_s3(s3_bucket=config['s3_bucket'], output_path=output_path,  target_directory=target_directory, only_metadata=only_metadata)
    if args.command in ['split_into_frames', 'do_local', 'do_s3']:
        split_into_frames(output_path=output_path, target_directory=target_directory, frame_interval=config['frame_interval'], video_range_train=video_range_train, video_range_test=video_range_test)
    if args.command in ['upload_frames_to_s3', 'do_s3']:
        upload_frames_to_s3(s3_bucket=config['s3_bucket'], output_path=output_path,  target_directory=target_directory)