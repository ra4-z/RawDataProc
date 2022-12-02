import os
import cv2
import json
from tqdm import tqdm

def read_raw_json(gt_dir):
    ''' 
        function:
            read json from gt_dir
        params: 
            gt_dir: the directory of the json files
        return:
            a dict of {camera_id, ordered_gt}
                ordered_gt: a dict, key is frame_id in order, value is a list of dict, each dict is a car's info
    '''
    gt = dict()
    cam_id = None
    for file in os.listdir(gt_dir):
        if file.endswith(".json"):
            # extract data from file
            with open(os.path.join(gt_dir, file), 'r') as fj:
                data = json.load(fj)["payload"]["class_prop"]["data"]
                # maybe -1 is needed for starting from 0
                frame_id = data[0]["frame_id"]
                if cam_id is None:
                    cam_id = data[0]["cam_id"]
            # add them to gt
            gt[frame_id] = []
            for car in data[0]["objects"]:
                # extract info
                car_info = dict()
                car_info["id"] = car["identity"]
                car_info["cover"] = car["covered_percent"]
                car_info["reliable"] = car["reliable"]
                # if car["reliable"]:
                #     print(f"{frame_id} {car['identity']}")
                car_info["confidence"] = car["confidence"]
                car_info["color"] = [c for _, c in car["color"].items()]
                car_info["bbox"] = [
                    c for _, c in car["box"].items()]  # x1, y1, x2, y2
                car_info["direction"] = [
                    d for _, d in car["direction"].items()]
                gt[frame_id].append(car_info)
    ordered_gt = dict()
    for key in sorted(gt):
        ordered_gt[key] = gt[key]
    return {cam_id: ordered_gt}


def video2imgs(video, save_dir, interval=1, format="jpeg"):
    cap = cv2.VideoCapture(video)
    frame_id = 0
    while(cap.isOpened):
        frame_id += 1
        ret, frame = cap.read()
        if ret == False:
            print(f"{video} is finished at {frame_id}!")
            return
        if frame_id % interval != 0:
            continue
        save_path = os.path.join(save_dir, f"{frame_id:05}.{format}")
        cv2.imwrite(save_path, frame)

    print(__name__, " is done!")
