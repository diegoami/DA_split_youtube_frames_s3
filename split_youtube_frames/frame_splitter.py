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
            grp_retrieved = list(retrieve_groups_from_desc(full_file))
            desc_map[sanitize_filename(file_core, restricted=True)] = grp_retrieved
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

    def getFrame(vidcap, sec, imgdir):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            cv2.imwrite(os.path.join(imgdir, "image" + str(count) + ".jpg"), image)  # save frame as JPG file
        return hasFrames

    sec = 0
    frameRate = frame_interval  # //it will capture image in each 0.5 second
    count = 1
    success = getFrame(vidcap, sec, img_output)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(vidcap, sec, img_output)


def retrieve_groups_from_desc(filename):
    with open(filename, 'r') as f:
        desc_curr_lines = f.readlines()
    desc_matching = [x for x in desc_curr_lines if re.match(RE_FIND_EXPR, x)]
    for dsc_m in desc_matching:
        match = re.match(RE_FIND_EXPR, dsc_m)
        yield match.groupdict()
