import os
import json
from tqdm import tqdm
import copy


def toMOT(data,
          save_dir,
          save_id=False,
          save_type=False,
          save_direction=False,
          interval=1):
    '''
        function:
            convert the data to MOT format
            [fn, id, x1, y1, w, h, type_id,
                direction_reliabilty, direction_x, direction_y]
        params:
            data: the data to be converted
            save_dir: the directory to save the converted data
            save_id: whether to save the id of the car
            save_type: whether to save the type of the car
            save_direction: whether to save the direction of the car
            interval: the interval of frame when saving data
        return:
            None
    '''
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    if not save_id:
        fixed_id = -1

    for cam in data:
        print("Processing camera ", cam)
        cnt = 0
        with open(os.path.join(save_dir, f"{cam}.txt"), 'w') as f:
            for frame in tqdm(data[cam]):
                cnt += 1
                if cnt % interval:  # 不在interval上就跳过
                    continue
                for car in data[cam][frame]:
                    if not save_id:
                        car["id"] = fixed_id
                    if not save_type:
                        car["type"] = 0
                    if not save_direction:
                        car["reliable"] = 0
                        car["direction"] = [0, 0]
                    f.write(f"{frame},{car['id']},")
                    f.write(
                        f"{car['bbox'][0]}, {car['bbox'][1]}, {car['bbox'][2]-car['bbox'][0]}, {car['bbox'][3]-car['bbox'][1]},")
                    f.write(f"{car['type']},")
                    # if car['reliable']:
                    #     print(("1"))
                    f.write(
                        f"{int(car['reliable'])},{car['direction'][0]},{car['direction'][1]}\n")


def toLABELME(data,
              version="5.1.1",
              save_dir=None,
              interval=1,
              pic_format="jpeg",
              ):
    def new_json(shapes=[],
                 imagePath=None,
                 imageData=None,
                 imageHeight=1080,
                 imageWidth=1920,
                 ):
        basic_info = dict()
        basic_info["vesrion"] = version
        basic_info["flags"] = {}
        basic_info["shapes"] = shapes
        basic_info["imagePath"] = imagePath
        basic_info["imageData"] = imageData
        basic_info["imageHeight"] = imageHeight
        basic_info["imageWidth"] = imageWidth
        basic_info = copy.deepcopy(basic_info)
        return basic_info

    def new_shape(label=None,
                  points=[],
                  group_id=None,
                  shape_type=None,
                  flags={}):
        shape = dict()
        shape["label"] = label
        shape["points"] = points
        shape["group_id"] = group_id
        shape["shape_type"] = shape_type
        shape["flags"] = flags
        shape = copy.deepcopy(shape)
        return shape

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    cnt = 0
    for cam in data:
        print("Processing camera ", cam)
        if not os.path.exists(os.path.join(save_dir, cam)):
            os.mkdir(os.path.join(save_dir, cam))

        for frame in tqdm(data[cam]):
            cnt += 1
            if cnt % interval:  # 不在interval上就跳过
                continue
            frame_json = new_json(imagePath=f"{cnt:05}.{pic_format}")
            for car in data[cam][frame]:
                shape = new_shape(label=f"{car['id']}",
                                  points=[car["bbox"][0:2], car["bbox"][2:4]],
                                  group_id=car['id'],
                                  shape_type="rectangle")
                frame_json["shapes"].append(shape)
            with open(os.path.join(save_dir, f"{cam}", f"{cnt:05}.json"), 'w') as f:
                json.dump(frame_json, f)


if __name__ == "__main__":
    from utils import read_raw_json
    cams = [1, 2, 4, 12, 13, 14, 19, 23, 26, 27,
            28, 30, 37, 55, 57, 59, 62, 64, 65, 66, 73]
    interval = 8
    for cam in cams:
        gt_dir = f"/data/codes/RawDataProc/data/yk{cam}_output"
        data = read_raw_json(gt_dir)
        toMOT(data, "/data/codes/RawDataProc/data/mot",
              save_id=True, save_direction=False, interval=interval)

        save_dir = "/data/codes/RawDataProc/data/labelme"
        toLABELME(data, save_dir=save_dir, interval=interval)
