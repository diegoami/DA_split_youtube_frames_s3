import boto3
from boto3.s3.transfer import S3Transfer
import os
import logging
from .utils import keep_groups_in_desc
from botocore.errorfactory import ClientError
from botocore.config import Config
boto3.set_stream_logger('', logging.DEBUG)

def upload_videos_to_s3(s3_bucket, output_path, target_directory, only_metadata=False):
    if s3_bucket:
        config = Config(s3={"use_accelerate_endpoint": True})
        s3_client = boto3.client('s3', region_name="eu-central-1", config=config)
        transfer = S3Transfer(s3_client)


    def upload_to_s3(full_file, dest_file):
        if dest_file:
            logging.info("Trying to transfer {} to {}:{}".format(full_file, s3_bucket, dest_file))
            try:
                s3_client.head_object(Bucket=s3_bucket, Key=dest_file)
                logging.info("{}:{} exists... skipping...".format(s3_bucket, dest_file))
            except ClientError:
                logging.info("Transfer in progress...".format(full_file, s3_bucket, dest_file))
                transfer.upload_file(full_file, s3_bucket, dest_file)
                logging.info("Done")


    playlist_output = os.path.join(output_path, target_directory)
    if s3_client:
        video_output = os.path.join(playlist_output, 'videos')
        metadata_output = os.path.join(playlist_output, 'metadata')
        video_files = os.listdir(video_output)
        metadata_files = os.listdir(metadata_output)
        for video_file in video_files:
            full_video_file = os.path.join(video_output, video_file)
            dest_file = os.path.join(target_directory, 'videos', video_file)
            upload_to_s3(full_video_file, dest_file)
        for metadata_file in metadata_files:
            full_metadata_file = os.path.join(playlist_output, metadata_file)
            dest_file = os.path.join(target_directory, 'metadata', metadata_file)
            upload_to_s3(full_metadata_file, dest_file)


def upload_frames_to_s3(s3_bucket, frame_output, frame_key):
    if s3_bucket:
        s3_client = boto3.client('s3')
        transfer = S3Transfer(s3_client)
    if s3_client:

        frame_dirs = os.listdir(frame_output)
        for frame_dir in frame_dirs:
            files = os.listdir(os.path.join(frame_output, frame_dir))
            for file in files:
                full_file = os.path.join(frame_output, frame_dir, file)
                dest_file = os.path.join('images', frame_key, frame_dir, file)
                logging.info("Transferring {} to {}:{}".format(full_file, s3_bucket, dest_file))
                transfer.upload_file(full_file, s3_bucket, dest_file)
