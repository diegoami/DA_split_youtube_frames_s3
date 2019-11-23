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