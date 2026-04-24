import cv2
import numpy as np

START_X, START_Y = 15, 15
W, H = 50, 50
GAP_X, GAP_Y = 35, 35

ROWS = 2
COLS = 4


def generate_boxes():
    boxes = []

    for r in range(ROWS):
        for c in range(COLS):
            x1 = START_X + c * (W + GAP_X)
            y1 = START_Y + r * (H + GAP_Y)
            x2 = x1 + W
            y2 = y1 + H
            boxes.append((x1, y1, x2, y2))

    return boxes


def crop_images(img, boxes):
    crops = []
    centers = []

    for (x1, y1, x2, y2) in boxes:
        crop = img[y1:y2, x1:x2]
        crops.append(crop)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        centers.append((cx, cy))
    return crops, centers


def extract_feature(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

    edges = cv2.Canny(th, 50, 150)

    return np.array([
        np.sum(edges > 0),
        np.sum(th == 0)
    ], dtype=np.float32)


def find_most_different(crops):
    features = np.array([extract_feature(c) for c in crops])

    diff = []
    for i in range(len(features)):
        d = np.mean(np.linalg.norm(features[i] - features, axis=1))
        diff.append(d)

    return int(np.argmax(diff))


def process_chinese_diff(img):
    boxes = generate_boxes()
    crops, centers = crop_images(img, boxes)

    idx = find_most_different(crops)
    return [(int(boxes[idx][0] + boxes[idx][2] // 2 / 330 * 380)), (boxes[idx][1] + boxes[idx][3]) // 2]
