import cv2
import os
import re
from youtube_dl.utils import sanitize_filename


RE_FIND_EXPR = "(?P<start>[\d:]+)-(?P<end>[\d:]+)\s+(?P<cat>\w+)\s+.*"


def split_into_frames(frame_output, playlist_output, frame_interval):
    files = list(os.listdir(playlist_output))
    desc_map = {}
    video_files = []
    for file in files:
        full_file = os.path.join(playlist_output, file)
        file_core, file_extension = os.path.splitext(file)
        if file_extension == '.dsc':
            grp = list(retrieve_groups_from_desc(full_file))
            desc_map[sanitize_filename(file_core, restricted=True)] = grp
        else:
            video_files.append(file)

    for file in video_files:
        full_file = os.path.join(playlist_output, file)
        file_core, file_extension = os.path.splitext(file)
        desc_categories = desc_map[file_core]
        extract_frames(file, frame_interval, frame_output, full_file, desc_categories)


def extract_frames(file, frame_interval, frame_output, full_file, desc_categories=None):
    vidcap = cv2.VideoCapture(full_file)
    img_output = os.path.join(frame_output, file)
    os.makedirs(img_output, exist_ok=True)

    def get_category(sec, desc_categories):
        found_secs = [tslot for tslot in desc_categories if tslot['start'] < sec < tslot['end']]
        if found_secs:
            category = found_secs[0]["cat"]
            return category
        return None

    def get_frame(vidcap, sec, imgdir, category='unknown'):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        os.makedirs(os.path.join(imgdir, category), exist_ok=True)
        to_save = os.path.join(imgdir, category, "image" + str(sec) + ".jpg")
        if hasFrames:
            cv2.imwrite(to_save, image)  # save frame as JPG file
        return hasFrames

    sec = 0
    frameRate = frame_interval  # //it will capture image in each 0.5 second
    count = 1
    category = get_category(sec, desc_categories)
    success = get_frame(vidcap, sec, img_output, category if category else "unknown")
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        category = get_category(sec, desc_categories)
        success = get_frame(vidcap, sec, img_output, category if category else "unknown")


def retrieve_groups_from_desc(filename):
    def youtube_time_to_secs(ytt):
        tus = ytt.split(':')[::-1]
        secs = 0
        for index, tu in enumerate(tus):
            secs += int(tu)*(60**index)
        return secs

    with open(filename, 'r') as f:
        desc_curr_lines = f.readlines()
    desc_matching = [x for x in desc_curr_lines if re.match(RE_FIND_EXPR, x)]
    for dsc_m in desc_matching:
        match = re.match(RE_FIND_EXPR, dsc_m)
        grp = match.groupdict()
        grp["start"], grp["end"] = youtube_time_to_secs(grp["start"]), youtube_time_to_secs(grp["end"])
        yield grp
