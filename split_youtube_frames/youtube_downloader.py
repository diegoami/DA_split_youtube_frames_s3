import logging
import os
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL

def get_int_video_ranges(video_ranges):
    videos_selection = []
    video_ranges_l = video_ranges.split(',')
    for vr in video_ranges_l:
        if '-' in vr:
            vr_l = vr.split('-')
            videos_selection.extend([x for x in range(int(vr_l[0]), int(vr_l[1])+1)])
        else:
            videos_selection.append(int(vr))
    return videos_selection

def download_videos(youtube_client, playlist_id, playlist_key, video_output_path, video_format, video_ranges):
    playlist_output = os.path.join(video_output_path, playlist_key)
    logging.info("Downloading from playlist {} to {}".format(playlist_key, playlist_output))
    if video_ranges:
        video_sel = get_int_video_ranges(video_ranges)
    else:
        video_sel = None
    index = 1
    for video_items in youtube_client.iterate_videos_in_playlist(playlist_id):
        logging.info(f"Trying to Downloading {index+1} video")
        for item in video_items['items']:
            snippet = item['snippet']
            content_details = item['contentDetails']
            video_id = content_details['videoId']
            title = snippet['title']
            print(video_id, title)
            video_info = youtube_client.get_video(video_id)
            url = "http://www.youtube.com/watch?v={}".format(video_id)
            if not video_sel or index in video_sel:
                logging.info(f"Downloading {index}th of playlist ")
                with YoutubeDL({'format': str(video_format), 'merge-output-format': 'mp4', 'cachedir': False,
                                'outtmpl': playlist_output + '/' + DEFAULT_OUTTMPL, "nooverwrites": True, "restrictfilenames": True}) as youtube_dl:
                    youtube_dl.download([url])
            else:
                logging.info(f"Skipping {index}th of playlist ")
            index += 1
    return playlist_output
