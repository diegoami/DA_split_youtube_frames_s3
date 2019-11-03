import cv2
import os


def split_into_frames(frame_output, playlist_output, frame_interval):
    files = os.listdir(playlist_output)
    for file in files:
        full_file = os.path.join(playlist_output, file)
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
