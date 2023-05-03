import cv2
import os


def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("not capped")
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0
    
    while True:
        ret, frame = cap.read()
        if ret:
            if n%1!=0: # これを変えて
                n += 1
                continue
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            print("finish")
            return

save_all_frames("make_data\\movie\\cloud001.mp4", "data\\img\\cloud_joker_1", "cloud_joker")
