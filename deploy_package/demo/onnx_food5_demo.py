from pathlib import Path
import cv2
import numpy as np
import onnxruntime as ort


MODEL_PATH = Path(r"D:\Projects\food_yolo_3516\models\food5_yolov5s_640\best.onnx")
IMAGE_PATH = Path(r"D:\Projects\food_yolo_3516\food5_dataset\images\val\ice_cream_00149.jpg")
SAVE_PATH = Path(r"D:\Projects\food_yolo_3516\onnx_demo_result.jpg")

CLASS_NAMES = [
    "chicken_wings",
    "dumplings",
    "fried_rice",
    "hamburger",
    "ice_cream",
]


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114)):
    """
    YOLOv5 预处理：
    保持原图比例缩放，不够的地方补灰边。
    返回：
    - 处理后的图
    - 缩放比例
    - 左右/上下补边
    """
    shape = img.shape[:2]  # h, w
    h0, w0 = shape
    new_h, new_w = new_shape

    r = min(new_h / h0, new_w / w0)
    resized_w = int(round(w0 * r))
    resized_h = int(round(h0 * r))

    dw = new_w - resized_w
    dh = new_h - resized_h

    dw /= 2
    dh /= 2

    if (w0, h0) != (resized_w, resized_h):
        img = cv2.resize(img, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)

    top = int(round(dh - 0.1))
    bottom = int(round(dh + 0.1))
    left = int(round(dw - 0.1))
    right = int(round(dw + 0.1))

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return img, r, (left, top)


def xywh_to_xyxy(box):
    x, y, w, h = box
    return np.array([
        x - w / 2,
        y - h / 2,
        x + w / 2,
        y + h / 2,
    ], dtype=np.float32)


def nms(boxes, scores, iou_thres=0.45):
    """
    简单 NMS：去掉重复框。
    boxes: [N, 4], xyxy
    scores: [N]
    """
    if len(boxes) == 0:
        return []

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
    order = scores.argsort()[::-1]

    keep = []

    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        inter_w = np.maximum(0, xx2 - xx1)
        inter_h = np.maximum(0, yy2 - yy1)
        inter = inter_w * inter_h

        union = areas[i] + areas[order[1:]] - inter + 1e-6
        iou = inter / union

        inds = np.where(iou <= iou_thres)[0]
        order = order[inds + 1]

    return keep


def main():
    print("model:", MODEL_PATH)
    print("image:", IMAGE_PATH)

    session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

    input_info = session.get_inputs()[0]
    output_info = session.get_outputs()[0]

    print("\n====== ONNX 输入输出信息 ======")
    print("input name :", input_info.name)
    print("input shape:", input_info.shape)
    print("input type :", input_info.type)
    print("output name :", output_info.name)
    print("output shape:", output_info.shape)
    print("output type :", output_info.type)

    img0 = cv2.imread(str(IMAGE_PATH))
    if img0 is None:
        raise FileNotFoundError(f"图片读取失败: {IMAGE_PATH}")

    img, ratio, pad = letterbox(img0, new_shape=(640, 640))

    # BGR -> RGB, HWC -> CHW, 归一化到 0~1
    img_input = img[:, :, ::-1].transpose(2, 0, 1)
    img_input = np.ascontiguousarray(img_input, dtype=np.float32) / 255.0
    img_input = img_input[None]  # [1, 3, 640, 640]

    outputs = session.run(None, {input_info.name: img_input})
    pred = outputs[0]

    print("\n====== 推理输出 ======")
    print("raw output shape:", pred.shape)

    # 通常 pred shape 是 [1, 25200, 10]
    pred = pred[0]

    conf_thres = 0.25
    iou_thres = 0.45

    boxes = []
    scores = []
    class_ids = []

    for det in pred:
        box = det[:4]
        obj_conf = det[4]
        class_scores = det[5:]

        class_id = int(np.argmax(class_scores))
        class_conf = class_scores[class_id]
        score = float(obj_conf * class_conf)

        if score < conf_thres:
            continue

        xyxy = xywh_to_xyxy(box)

        # 去掉 letterbox 的 padding，再缩放回原图坐标
        left, top = pad
        xyxy[[0, 2]] -= left
        xyxy[[1, 3]] -= top
        xyxy /= ratio

        h0, w0 = img0.shape[:2]
        xyxy[[0, 2]] = np.clip(xyxy[[0, 2]], 0, w0 - 1)
        xyxy[[1, 3]] = np.clip(xyxy[[1, 3]], 0, h0 - 1)

        boxes.append(xyxy)
        scores.append(score)
        class_ids.append(class_id)

    boxes = np.array(boxes, dtype=np.float32)
    scores = np.array(scores, dtype=np.float32)
    class_ids = np.array(class_ids, dtype=np.int32)

    keep = nms(boxes, scores, iou_thres=iou_thres)

    print("\n====== 检测结果 ======")
    if not keep:
        print("没有检测到目标")
    else:
        for idx in keep:
            cls_id = int(class_ids[idx])
            score = float(scores[idx])
            x1, y1, x2, y2 = boxes[idx].astype(int)

            print(f"{CLASS_NAMES[cls_id]}  conf={score:.3f}  box=({x1},{y1},{x2},{y2})")

            cv2.rectangle(img0, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                img0,
                f"{CLASS_NAMES[cls_id]} {score:.2f}",
                (x1, max(y1 - 5, 0)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

    cv2.imwrite(str(SAVE_PATH), img0)
    print("\n结果图片保存到:", SAVE_PATH)


if __name__ == "__main__":
    main()