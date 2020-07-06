# FRAME EXTRACTOR

## OVERVIEW

The goal is to extract frames from videos in a playlist in youtube and save, say, in S3, for further processing for machine learning goals

## REQUIREMENTS

* A google applications and its correspondent `client_secrets.json`
* set up configuration in config.yml

## SET UP VIDEO DESCRIPTION

The video description on youtube must contain text snippets in the following format

<start-time>:<end-time> <Category>

### CONFIGURATION IN CONFIG.YML 
* output_path: root of your work directory - where your video and images will be
* client_json_file: cloud credentials for authentication to youtube 
* video_format: what format to download your files
* s3_bucket: name of a s3 bucket
* frame_interval: every how many seconds create a frame
* playlist_id: playlist where your work videos are saved

Videos are ordered according to their title, that should contain the pattern E\d+ (for instance E22, E23.... for episode)
Based on that, this is how handles episode number videos

* video_range_keep: the episodes whose videos we want to keep
* video_range_train: the episodes we use for train
* video_range_test: the episodes we want to predict


## EXECUTION

`python main.py` can be called with the following arguments.`python main.py do_local` to execute the full workflow. 

* download_videos
* upload_videos_to_s3
* upload_frames_to_s3
* split_into_frames
* do_local
* do_s3

## RESULT

In your <output_path> directory you will find the subdirectories <frames> and <videos>. Videos that have been retrieved by youtube and the frames that have been generated will be separated into directories, based on the categories given in the videos' descriptions.
Frames from the videos to be predicted will be under a directory named "uncategorized"

## NEXT STEP

The next step after this generation is to create a model using the project https://github.com/diegoami/DA_tensorflow_for_letsplay
