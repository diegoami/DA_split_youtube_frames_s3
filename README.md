# FRAME EXTRACTOR

## OVERVIEW

The goal is to extract frames from videos in a playlist in youtube and save, say, in S3, for further processing for machine learning goals

## REQUIREMENTS

* A google applications and its correspondent `client_secrets.json`
* set up in config.yml the path to `output_dir` and your `client_secrets`
* Call `python main.py --playlist_id=<YOUR_PLAYLIST_ID`