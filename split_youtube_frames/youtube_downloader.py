import logging
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from youtube_dl.utils import sanitize_filename
from .utils import get_int_video_ranges, extract_episode_number
import pathlib
import os


def download_videos(youtube_client, playlist_id, playlist_key, video_output_path, video_format, video_range):
    playlist_output = os.path.join(video_output_path, playlist_key)
    os.makedirs(playlist_output, exist_ok=True)

    logging.info("Downloading from playlist {} to {}".format(playlist_key, playlist_output))
    if video_range:
        video_sel = get_int_video_ranges(video_range)
    else:
        video_sel = None
    index = 1
    for video_items in youtube_client.iterate_videos_in_playlist(playlist_id, maxCount=50):
        logging.info(f"Trying to Downloading {index+1} video")

        for item in video_items['items']:
            if not video_sel or index in video_sel:
                video_id = item['contentDetails']['videoId']
                video_snippet = youtube_client.get_video_snippet(video_id)
                description = video_snippet["description"]
                title = video_snippet["title"]
                description_updated(description, playlist_output, video_id, title)
                url = "http://www.youtube.com/watch?v={}".format(video_id)

                logging.info(f"Downloading {index}th of playlist... ")
                with YoutubeDL({'format': str(video_format), 'merge-output-format': 'mp4', 'cachedir': False,
                                'outtmpl': playlist_output + '/' + DEFAULT_OUTTMPL, "nooverwrites": True, "restrictfilenames": True}) as youtube_dl:
                    youtube_dl.download([url])
                logging.info(f"Done")

            else:
                logging.info(f"Skipping {index}th of playlist ")
            index += 1
    return playlist_output


def description_updated(description, playlist_output, video_id, title):

    description_filename = sanitize_filename(f'{title}-{video_id}.dsc', restricted=True)
    description_full_filename = os.path.join(playlist_output, description_filename)
    if os.path.isfile(description_full_filename):
        with open(description_full_filename, 'r') as dfwr:
            old_desc = "".join(dfwr.readlines())
            if old_desc != description:

                logging.info("Description for {} has changed".format(description_full_filename))
                episode = extract_episode_number(description_full_filename)
                e_snippet = "*E{}*.*".format(episode)

                epis_old_gen = pathlib.Path(playlist_output).rglob(e_snippet)
                for epis_old in epis_old_gen:
                    logging.info("Removing {}".format(epis_old))
                    os.remove(epis_old)
    with open(os.path.join(playlist_output, description_filename), 'w') as dfw:
        dfw.writelines(description)
        logging.info(f"Description saved to {description_filename}")

