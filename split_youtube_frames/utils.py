import re

RE_EPIS_EXPR = ".*_E(?P<episode>\d+)_.*"

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


def extract_episode_number(file_name):
    match = re.match(RE_EPIS_EXPR, file_name)
    eps_dict = match.groupdict()
    episode = int(eps_dict["episode"])
    return episode