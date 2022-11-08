import array
import io
import struct
import time
import traceback

import cv2.cv2 as cv2
import numpy
import numpy as np
import copy
import sys
import traceback
img_path="airplane.jpeg"

scale_ratio = 0.0
scale_dw = 0
scale_dh = 0
img_height = 0
img_width = 0
from io import BytesIO


def array_to_bytes(x: np.ndarray) -> bytes:
    np_bytes = BytesIO()
    np.save(np_bytes, x, allow_pickle=True)
    return np_bytes.getvalue()


def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=False, scaleFill=False, scaleup=True, stride=32):
    shape = img.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:
        r = min(r, 1.0)
    ratio = r, r

    new_unpad = int(round(shape[1] * r)), int(round(shape[0]) * r)
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    if auto:
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)
    elif scaleFill:
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]

    dw /= 2
    dh /= 2
    if shape[::-1] != new_unpad:
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    global scale_ratio
    scale_ratio = r

    global scale_dw
    scale_dw = dw

    global scale_dh
    scale_dh = dh

    return img, ratio, (dw, dh)


def get_input_tensor():
    try:
        #input = np.frombuffer(dataList[0].getData(), np.uint8)
        #src_img = cv2.imdecode(input, cv2.IMREAD_COLOR)

        src_img = cv2.imread(img_path)

        global img_height
        img_height = src_img.shape[0]
        global img_width
        img_width = src_img.shape[1]

        img_size = (640, 640)
        img = letterbox(src_img, img_size, stride=32)[0]

        # convert
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = img.astype(dtype=np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        return img
    except Exception as e:
        print(traceback.print_exc())


def get_result_classify(input):
    # x = []
    # for i in range(2142000):
    #     data = input[i * 4:(i * 4) + 4]
    #     a = struct.unpack('f', data)
    #     x.append(float(a[0]))
    # print(x[0], "\n")
    score_threshold = 0.25
    classes = [
        "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
        "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
        "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
        "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
        "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
        "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
        "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
        "scissors", "teddy bear", "hair drier", "toothbrush"
    ]
    temp = np.frombuffer(input, dtype=np.float32)
    npConfidence = temp.copy()
    npConfidence.resize((1, 25200, 85))
    print("get_result_classify frist value: \n", npConfidence[0][0][0], flush=True)
    num_anchors = len(npConfidence[0])
    src_img = cv2.imread(img_path)

    max_score = 0
    result = {}
    for i in range(num_anchors):
        obj_conf = npConfidence[0][i][4]
        if obj_conf < score_threshold:
            continue
        cls_conf = max(list(npConfidence[0][i][5:]))
        label = list(npConfidence[0][i][5:]).index(cls_conf)

        conf = obj_conf * cls_conf
        if conf < score_threshold:
            continue

        cx = npConfidence[0][i][0]
        cy = npConfidence[0][i][1]
        w = npConfidence[0][i][2]
        h = npConfidence[0][i][3]
        x1 = ((cx - w / 2.0) - scale_dw) / scale_ratio
        y1 = ((cy - h / 2.0) - scale_dh) / scale_ratio
        x2 = ((cx + w / 2.0) - scale_dw) / scale_ratio
        y2 = ((cy + h / 2.0) - scale_dh) / scale_ratio

        box_x1 = max(0.0, x1)
        box_y1 = max(0.0, y1)
        box_x2 = min(x2, img_width - 1.0)
        box_y2 = min(y2, img_height - 1.0)
        box_score = conf
        box_label = label
        box_label_text = classes[label]

        if box_score > max_score:
            max_score = box_score
            result = {
                "label": box_label_text,
                "score": max_score,
                "box": [box_x1, box_y1, box_x2, box_y2],
            }

        print(box_label_text, box_score, box_label, flush=True)
        # tmpimg = copy.deepcopy(src_img)
        # cv2.rectangle(tmpimg, (int(box_x1), int(box_y1)), (int(box_x2), int(box_y2)), (255, 255, 255), thickness=2)
        # cv2.putText(tmpimg, box_label_text + ": " + str(box_score),
        #             (int((box_x1 + box_x2) / 2), int((box_y1 + box_y2) / 2)), cv2.FONT_HERSHEY_COMPLEX, 0.7,
        #             (0, 255, 0), thickness=2)
        # cv2.imwrite(r"./test/dog_rlt_" + str(i) + ".jpg", tmpimg)
        print(result)
    return result


