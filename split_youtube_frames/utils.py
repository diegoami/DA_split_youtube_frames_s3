import re

RE_EPIS_EXPR = ".* E(?P<episode>\d+).*"
RE_FIND_EXPR = "(?P<start>[\d:]+)-(?P<end>[\d:]+)\s+(?P<cat>\w+)[\s\:]+.*"


def get_int_video_ranges(video_ranges):
    if not video_ranges:
        return {}
    elif isinstance(video_ranges, int):
        return {video_ranges}
    else:
        videos_selection = []
        video_ranges_l = video_ranges.split(',')
        for vr in video_ranges_l:
            if '-' in vr:
                vr_l = vr.split('-')
                videos_selection.extend([x for x in range(int(vr_l[0]), int(vr_l[1])+1)])
            else:
                videos_selection.append(int(vr))
        return set(videos_selection)


def extract_episode_number(file_name):
    match = re.match(RE_EPIS_EXPR, file_name)
    eps_dict = match.groupdict()
    episode = int(eps_dict["episode"])
    return episode


def youtube_time_to_secs(ytt):
    tus = ytt.split(':')[::-1]
    secs = 0
    for index, tu in enumerate(tus):
        secs += int(tu)*(60**index)
    return secs


def keep_groups_in_desc(filename):
    with open(filename, 'r') as f:
        desc_curr_lines = f.readlines()
    desc_matching = [x for x in desc_curr_lines if re.match(RE_FIND_EXPR, x)]
    newfilename = filename.replace('.dsc', '.prd')
    if len(desc_matching) > 0:
        with open(newfilename, 'w') as f:
            f.writelines(desc_matching)
    return newfilename

def retrieve_groups_from_desc(filename):


    with open(filename, 'r') as f:
        desc_curr_lines = f.readlines()
    desc_matching = [x for x in desc_curr_lines if re.match(RE_FIND_EXPR, x)]
    for dsc_m in desc_matching:
        match = re.match(RE_FIND_EXPR, dsc_m)
        grp = match.groupdict()
        grp["start"], grp["end"] = youtube_time_to_secs(grp["start"]), youtube_time_to_secs(grp["end"])
        yield grp