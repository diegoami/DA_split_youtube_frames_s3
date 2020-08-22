import logging
from youtube_dl import YoutubeDL, DEFAULT_OUTTMPL
from youtube_dl.utils import sanitize_filename
from .utils import get_int_video_ranges, extract_episode_number
import pathlib
import os
from .utils import keep_groups_in_desc

def remove_files_for_episode(playlist_output, episode):
    e_snippet = "*E{}*.*".format(episode)
    epis_old_gen = pathlib.Path(playlist_output).rglob(e_snippet)
    for epis_old in epis_old_gen:
        logging.info("Removing {}".format(epis_old))
        os.remove(epis_old)

def download_videos(youtube_client, playlist_ids, video_output_path, metadata_output_path, video_format, video_range_keep, video_range_train, video_range_test):

    def download_video(directory, video_id):
        url = "http://www.youtube.com/watch?v={}".format(video_id)
        with YoutubeDL({'format': str(video_format), 'merge-output-format': 'mp4', 'cachedir': False,
                        'outtmpl': directory + '/' + DEFAULT_OUTTMPL, "nooverwrites": True, "restrictfilenames": True}) as youtube_dl:
            youtube_dl.download([url])
        logging.info(f"Done")
    os.makedirs(video_output_path, exist_ok=True)

    video_sel_keep = get_int_video_ranges(video_range_keep)
    video_sel_train = get_int_video_ranges(video_range_train)
    video_sel_test = get_int_video_ranges(video_range_test)
    for playlist_id in playlist_ids:
        logging.info(f"Processing playlist : {playlist_id}")
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
                    remove_files_for_episode(video_output_path, episode)
                    update_description(description=description, directory=metadata_output_path, video_id=video_id, title=title)
                    download_video(directory=video_output_path, video_id=video_id)
                elif episode in video_sel_test:
                    download_video(playlist_output=video_output_path, video_id=video_id)
            else:
                logging.info(f"Skipping {index}th of playlist ")
            index += 1



def update_description(description, directory, video_id, title):

    description_filename = sanitize_filename(f'{title}-{video_id}.dsc', restricted=True)
    full_filename = os.path.join(directory, description_filename)
    with open(full_filename, 'w') as dfw:
        if description:
            dfw.writelines(description)
            logging.info(f"Description saved to {description_filename}")

    keep_groups_in_desc(full_filename)