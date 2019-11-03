# FRAME EXTRACTOR

## OVERVIEW

The goal is to extract frames from videos in a playlist in youtube and save, say, in S3, for further processing for machine learning goals

## REQUIREMENTS

* A google applications and its correspondent `client_secrets.json`
* set up configuration in config.yml 

## EXECUTION

* `python main.py download_videos --playlist_id=<YOUR_PLAYLIST_ID>`
* `python main.py upload_videos_to_s3 --playlist_id=<YOUR_PLAYLIST_ID>`
* `python main.py split_into_frames --playlist_id=<YOUR_PLAYLIST_ID>`
* `python main.py upload_frames_to_s3 --playlist_id=<YOUR_PLAYLIST_ID>`