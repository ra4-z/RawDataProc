from utils import video2imgs
import os

video_file = "./data/yk1.mkv"
save_dir = "./data/yk1_imgs"

if __name__ == "__main__":
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    video2imgs(video_file, save_dir)
