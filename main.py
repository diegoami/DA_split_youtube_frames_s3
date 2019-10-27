import yaml
import argparse
import os
from youtube3 import YoutubeClient


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist_id', type=str)
    with open('config.yml') as f:
        config = yaml.safe_load(f)
        output_path = config['output_dir']
        client_json_file = config['client_json_file']
    youtube_client = YoutubeClient(os.path.join(os.path.dirname(__file__), client_json_file))
    args = parser.parse_args()
    playlist_id = args.playlist_id
    for video_items in youtube_client.iterate_videos_in_channel(playlist_id):
        for item in video_items['items']:
            print(item['snippet']['title'])


