import cv2
import os
import re
import shutil
import logging
from youtube_dl.utils import sanitize_filename
from .utils import extract_episode_number
from .utils import get_int_video_ranges
from .utils import youtube_time_to_secs
from .utils import keep_groups_in_desc
from .utils import retrieve_groups_from_desc



def split_into_frames(frame_output, playlist_output, frame_interval, video_range_train, video_range_test):
    os.makedirs(frame_output, exist_ok=True)
    files = list(os.listdir(playlist_output))
    valid_ranges_train = get_int_video_ranges(video_range_train)
    valid_ranges_test = get_int_video_ranges(video_range_test)
    desc_map = {}
    video_files = []
    for file in files:
        full_file = os.path.join(playlist_output, file)
        file_core, file_extension = os.path.splitext(file)
        if file_extension == '.dsc':
            grp = list(retrieve_groups_from_desc(full_file))
            desc_map[sanitize_filename(file_core, restricted=True)] = grp
        else:
            episode = extract_episode_number(file)
            if episode in valid_ranges_train or episode in valid_ranges_test:
                logging.info("Processing {} episode".format(episode))
                video_files.append(file)
            else:
                logging.info("Skipping {} episode".format(episode))

    test_dir = os.path.join(frame_output, 'test')
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)
    for file in video_files:
        full_file = os.path.join(playlist_output, file)
        file_core, file_extension = os.path.splitext(file)
        desc_categories = desc_map.get(file_core, None)
        extract_frames(file, frame_interval, frame_output, full_file, desc_categories)


def extract_frames(file, frame_interval, frame_output, full_file, desc_categories=None):
    vidcap = cv2.VideoCapture(full_file)


    def get_category(sec, desc_categories):
        found_secs = [tslot for tslot in desc_categories if tslot['start'] < sec < tslot['end']]
        if found_secs:
            category = found_secs[0]["cat"]
            return category
        return None

    def get_frame(vidcap, sec, imgdir, episode, category, dir_to_split):

        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        os.makedirs(os.path.join(imgdir, dir_to_split, category), exist_ok=True)
        to_save = os.path.join(imgdir,  dir_to_split, category, "E_{:>04d}_{:>06d}.jpg".format(episode, sec))
        if hasFrames:
            cv2.imwrite(to_save, image)
        return hasFrames

    sec = 0
    episode = extract_episode_number(file)
    frameRate = frame_interval
    count = 0
    success = True
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        if desc_categories:
            category = get_category(sec, desc_categories)
            dir_to_split = 'validation' if (count % 5 == 0) else 'train'
            category = category if category else "unknown"
        else:
            dir_to_split = 'test'
            category = 'uncategorized'
        success = get_frame(vidcap, sec, frame_output, episode, category, dir_to_split)




