import itertools

import cv2
import numpy as np


def getSize(p):
    sum_rows = p.shape[0]
    sum_cols = p.shape[1]
    channels = p.shape[2] if len(p.shape) > 2 else 1
    return sum_rows, sum_cols, channels


def merge(sum_rows, sum_cols, channels, p1, p2, p3, p4):
    final_matrix = np.zeros((sum_rows, sum_cols, channels), np.uint8)
    part_rows, part_cols = sum_rows // 2, sum_cols // 2

    final_matrix[0:part_rows, 0:part_cols] = p1
    final_matrix[0:part_rows, part_cols:sum_cols] = p2
    final_matrix[part_rows:sum_rows, 0:part_cols] = p3
    final_matrix[part_rows:sum_rows, part_cols:sum_cols] = p4
    return final_matrix


def get_diff_ele(list1, list2):
    if len(list1) != len(list2):
        return True
    diff_list = []
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            diff_list.append(list2[i])
    return diff_list


def get_correct_arr(content):
    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    sum_rows, sum_cols, channels = getSize(img)

    part_rows, part_cols = sum_rows // 2, sum_cols // 2

    part1 = img[0:part_rows, 0:part_cols]
    part2 = img[0:part_rows, part_cols:sum_cols]
    part3 = img[part_rows:sum_rows, 0:part_cols]
    part4 = img[part_rows:sum_rows, part_cols:sum_cols]

    pieces = [
        [0, part1],
        [1, part2],
        [2, part3],
        [3, part4]
    ]

    result = itertools.permutations(pieces, 4)

    best_line_count = float('inf')
    best_result = None

    for x in result:

        diff_ele_list = get_diff_ele(
            [0, 1, 2, 3],
            [x[0][0], x[1][0], x[2][0], x[3][0]]
        )

        if len(diff_ele_list) > 2:
            continue

        f = merge(sum_rows, sum_cols, channels,
                  x[0][1], x[1][1], x[2][1], x[3][1])

        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 35, 80, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 0.01, np.pi / 360, 60,
                                minLineLength=50, maxLineGap=10)

        line_count = len(lines) if lines is not None else 0

        # 找到完全无直线（认为正确）
        if lines is None:
            best_result = [x[0][0], x[1][0], x[2][0], x[3][0]]
            break

        # 记录最优
        if line_count < best_line_count:
            best_line_count = line_count
            best_result = [x[0][0], x[1][0], x[2][0], x[3][0]]

    target_pos = {0: 0, 1: 1, 2: 2, 3: 3}
    need_move = []
    for current_pos, piece_id in enumerate(best_result):
        correct_pos = target_pos[piece_id]
        if current_pos != correct_pos:
            need_move.append(correct_pos)

    return best_result, need_move
