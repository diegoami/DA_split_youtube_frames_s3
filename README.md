# FRAME EXTRACTOR

## OVERVIEW

The goal is to extract frames from videos in a playlist in youtube and save, say, in S3, for further processing for machine learning goals

## REQUIREMENTS

* A google applications and its correspondent `client_secrets.json`
* set up configuration in config.yml 

## EXECUTION

`python main.py` can be called with the following arguments.`python main.py do_local` to execute the full workflow. 

* download_videos
* upload_videos_to_s3
* upload_frames_to_s3
* split_into_frames
* do_local
* do_s3

