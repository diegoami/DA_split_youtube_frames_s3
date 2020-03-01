import logging
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from youtube_dl.utils import sanitize_filename
from .utils import get_int_video_ranges, extract_episode_number
import pathlib
import os


def remove_files_for_episode(playlist_output, episode):
    e_snippet = "*E{}*.*".format(episode)
    epis_old_gen = pathlib.Path(playlist_output).rglob(e_snippet)
    for epis_old in epis_old_gen:
        logging.info("Removing {}".format(epis_old))
        os.remove(epis_old)

def download_videos(youtube_client, playlist_id, playlist_key, video_output_path, video_format, video_range_keep, video_range_train, video_range_test):

    def download_video(playlist_output, video_id):
        url = "http://www.youtube.com/watch?v={}".format(video_id)
        logging.info(f"Downloading {index}th of playlist... ")
        with YoutubeDL({'format': str(video_format), 'merge-output-format': 'mp4', 'cachedir': False,
                        'outtmpl': playlist_output + '/' + DEFAULT_OUTTMPL, "nooverwrites": True, "restrictfilenames": True}) as youtube_dl:
            youtube_dl.download([url])
        logging.info(f"Done")

    playlist_output = os.path.join(video_output_path, playlist_key)
    os.makedirs(playlist_output, exist_ok=True)

    logging.info("Downloading from playlist {} to {}".format(playlist_key, playlist_output))

    video_sel_keep = get_int_video_ranges(video_range_keep)
    video_sel_train = get_int_video_ranges(video_range_train)
    video_sel_test = get_int_video_ranges(video_range_test)

    index = 1
    for video_items in youtube_client.iterate_videos_in_playlist(playlist_id, maxCount=50):
        logging.info(f"Trying to Downloading {index+1} video")

        for item in video_items['items']:
            video_id = item['contentDetails']['videoId']
            video_snippet = youtube_client.get_video_snippet(video_id)
            description = video_snippet["description"]
            title = video_snippet["title"]
            episode = extract_episode_number(sanitize_filename(title, restricted=True))
            if episode in video_sel_keep:
                pass
            elif episode in video_sel_train:
                remove_files_for_episode(playlist_output, episode)
                update_description(description=description, playlist_output=playlist_output, video_id=video_id, title=title)
                download_video(playlist_output=playlist_output, video_id=video_id)
            elif episode in video_sel_test:
                download_video(playlist_output=playlist_output, video_id=video_id)
        else:
            logging.info(f"Skipping {index}th of playlist ")
        index += 1
    return playlist_output


def update_description(description, playlist_output, video_id, title):

    description_filename = sanitize_filename(f'{title}-{video_id}.dsc', restricted=True)

    with open(os.path.join(playlist_output, description_filename), 'w') as dfw:
        if description:
            dfw.writelines(description)
            logging.info(f"Description saved to {description_filename}")

