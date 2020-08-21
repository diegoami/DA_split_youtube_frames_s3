import boto3
from boto3.s3.transfer import S3Transfer
import os
import logging


def upload_videos_to_s3(s3_bucket, playlist_output, playlist_key, target_directory):
    if not target_directory:
        target_directory = playlist_key
    if s3_bucket:
        s3_client = boto3.client('s3')
        transfer = S3Transfer(s3_client)
    if s3_client:

        files = os.listdir(playlist_output)
        for file in files:
            full_file = os.path.join(playlist_output, file)
            if '.mp4' in full_file:
                dest_file = os.path.join('videos', target_directory, file)
            else:
                dest_file = os.path.join('metadata', target_directory, file)
            logging.info("Transferring {} to {}:{}".format(full_file, s3_bucket, dest_file))
            transfer.upload_file(full_file, s3_bucket, dest_file)


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
