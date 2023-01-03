import yaml
import argparse
import os
import logging
import sys



from split_youtube_frames.frame_splitter import simple_split

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('configuration', help='configuration to run', default='config')

    args = parser.parse_args(sys.argv[1:2])
    configuration_file = f'{args.configuration}.yml'
    if not os.path.exists(configuration_file):
        print(f'{configuration_file} does not exist')
        exit(1)

    with open(configuration_file) as f:
        config = yaml.safe_load(f)

    args = parser.parse_args()
    video_range_keep = config.get('video_range_keep', None)
    video_range_train = config.get('video_range_train', None)
    category_mapping = config.get('category_mapping', None)

    video_output_path = config.get('video_output_path', None)
    frame_output_path = config.get('frame_output_path', None)
    if not os.path.exists(video_output_path):
        os.makedirs(video_output_path)
    if not os.path.exists(frame_output_path):
        os.makedirs(frame_output_path)


    simple_split(video_output=video_output_path,
                 frame_output=frame_output_path,
                 frame_interval=config['frame_interval'],
                 video_range_train=video_range_train)
