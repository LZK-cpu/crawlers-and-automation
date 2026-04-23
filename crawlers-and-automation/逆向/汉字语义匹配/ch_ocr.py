import os
import shutil
import time
import ddddocr
import numpy as np

from PIL import Image
from ultralytics import YOLO
from words import words_arr

model = YOLO('runs/detect/train/weights/best.pt')
extract_folder = 'extracted'
test_folder = 'testImage'


def extract_two_blocks(img_path, file_name, block1=(3, 10, 18, 25), block2=(18, 10, 33, 25), output_dir=extract_folder):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(img_path)

    char1 = img.crop(block1)
    char2 = img.crop(block2)
    save1 = os.path.join(output_dir, "char1_" + file_name)
    save2 = os.path.join(output_dir, "char2_" + file_name)

    # char1.show()
    char1.save(save1)
    # char2.show()
    char2.save(save2)


def extract_one_blocks(img_path, file_name, block1=(11, 10, 25, 24), output_dir=extract_folder):
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(img_path)

    char1 = img.crop(block1)
    save1 = os.path.join(output_dir, "char1_" + file_name)

    # char1.show()
    char1.save(save1)


def get_top(res, max_candidates=3, common_chars=None, dynamic_thresh_ratio=0.01):
    chars = res['charsets']
    probs = np.array(res['probability'])
    final_probs = probs.max(axis=0)
    pairs = [(c, p) for c, p in zip(chars, final_probs) if c.strip() != '']
    top1_prob = max(pairs, key=lambda x: x[1])[1]
    prob_thresh = max(0.01, top1_prob * dynamic_thresh_ratio)
    filtered = [(c, p) for c, p in pairs if p >= prob_thresh]
    if not filtered:
        filtered = [max(pairs, key=lambda x: x[1])]
    if common_chars is not None:
        filtered = [(c, p) for c, p in filtered if c in common_chars]
        if not filtered:
            filtered = [max(pairs, key=lambda x: x[1])]

    top_candidates = sorted(filtered, key=lambda x: x[1], reverse=True)[:max_candidates]

    return top_candidates


def match_question(answer, question):
    if answer in words_arr[question]:
        return True, question
    return False, ''


def answers_match_question(all_words, answer, question_word):
    for word in all_words:
        match, question = match_question(word, question_word)
        if match:
            return word + "==>" + question_word
    return answer + '==>无匹配'


def get_all_words(res1, res2=None):
    if res2:
        all_words = [c1 + c2 for c1, p1 in res1 for c2, p2 in res2]
    else:
        all_words = [c1 for c1, p1 in res1]
    return all_words


def get_text(img1, question_word, img2=None):
    res1 = ocr.classification(img1, probability=True)
    res1_top = get_top(res1)
    for c, p in res1_top:
        print(f"{c}==>{p:.6f}", end=' ')

    if img2:
        res2 = ocr.classification(img2, probability=True)
        res2_top = get_top(res2)
        for c, p in res2_top:
            print(f"{c}==>{p:.6f}", end=' ')
        answer = res1_top[0][0] + res2_top[0][0]
        match, question = match_question(answer, question_word)
        if match:
            return answer + "==>" + question
        else:
            all_words = get_all_words(res1_top, res2_top)
            return answers_match_question(all_words, answer, question_word)
    else:
        answer = res1_top[0][0]
        match, question = match_question(answer, question_word)
        if match:
            return answer + "==>" + question
        else:
            all_words = get_all_words(res1_top)
            return answers_match_question(all_words, answer, question_word)


def clear_floder(flider_name):
    if os.path.exists(flider_name):
        shutil.rmtree(flider_name)
    os.makedirs(flider_name)


ocr = ddddocr.DdddOcr(show_ad=False, beta=True, use_gpu=True, device_id=0)
ocr.set_ranges(7)


def get_mfamate():
    with open("question.png", "rb") as f:
        que_img = f.read()
    real_question = ocr.classification(que_img)
    print(real_question)
    real_answers = []
    for root, dirs, files in os.walk("./testImage"):
        for index, file in enumerate(files):
            path = os.path.join(root, file)
            r = model(path,verbose=False)
            char_num = len(r[0].boxes)
            if char_num == 1:
                extract_one_blocks(path, file)
                with open("./extracted/char1_" + file, "rb") as f:
                    img1 = f.read()
                    text = get_text(img1, real_question)
            else:
                extract_two_blocks(path, file)
                with open("./extracted/char1_" + file, "rb") as f:
                    img1 = f.read()
                with open("./extracted/char2_" + file, "rb") as f:
                    img2 = f.read()
                text = get_text(img1, real_question, img2)
            print(text)
            if text.split('==>')[1] != '无匹配':
                real_answers.append(file.split('.')[0])
    clear_floder(extract_folder)
    clear_floder(test_folder)
    return real_answers


