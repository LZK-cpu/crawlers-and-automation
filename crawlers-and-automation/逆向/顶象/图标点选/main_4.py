import json
import os
import random
import threading
import time

import cv2
import ddddocr
import execjs
import numpy as np
from requests import Session
from ultralytics import YOLO

from type_ak import appId_dict
from image_infer import similarity_content

ocr = ddddocr.DdddOcr(show_ad=False, det=False, beta=True)
model = YOLO("model/图标点选_runs/detect/train/weights/best.pt")
s = Session()
s.verify = False


def extract_numbers(icon_list):
    return [item.split('/')[-1].split('.')[0] for item in icon_list]


def run(type):
    ts = time.time()
    _t = str(int(ts // 3600))
    print(_t)
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "origin": "https://www.dingxiang-inc.com",
        "pragma": "no-cache",
        "referer": "https://www.dingxiang-inc.com/",
        "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }
    js_url = "https://cdn.dingxiang-inc.com/ctu-group/ctu-greenseer/greenseer.js"
    params = {
        "_t": _t
    }
    response = s.get(js_url, headers=headers, params=params)
    get_ac_js_code = response.text
    with open('main.js', 'w', encoding='utf-8') as f:
        f.write(get_ac_js_code)
    aid = 'dx-{}-63276804-11'.format(str(int(ts * 1000)))
    ak = appId_dict[type]
    cc = "6554343aU0MT73yU0M2yQGgeDMa2Xtr12D7gEwc1"
    cid = "88979385"
    jsv = "5.1.53"
    print(aid)
    url_path = "https://cap.dingxiang-inc.com/api/a?"
    params = {
        "w": "380",
        "h": "165",
        "s": "50",
        "ak": ak,
        "c": "",
        "jsv": jsv,
        "aid": aid,
        "wp": "1",
        "de": "0",
        "uid": "",
        "lf": "0",
        "tpc": "",
        "cid": cid,
        "_r": random.random()
    }
    url_a_res = s.get(url=url_path, headers=headers, params=params).json()
    sid = url_a_res.get("sid")
    print(sid)
    tp = url_a_res.get("tp1")
    bg_image_url = 'https://static4.dingxiang-inc.com/picture' + tp
    icons = json.loads(url_a_res.get("icons"))
    print(icons)

    img_array = np.frombuffer(s.get(bg_image_url).content, np.uint8)
    bg_image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    results = model(bg_image, verbose=False)

    points = []
    for icon in icons:
        with open('model/real_icons/' + icon.split('/')[-1], 'rb') as f:
            icon_bytes = f.read()
            sim = 0
            correct_points = None
            for i, box in enumerate(results[0].boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                point = int((x1 + x2) / 2 / 300 * 380), int((y1 + y2) / 2 / 150 * 165)
                crop = bg_image[y1:y2, x1:x2]
                crop = cv2.bitwise_not(crop)
                s_cur = similarity_content(icon_bytes, crop)
                if s_cur > sim:
                    sim = s_cur
                    correct_points = point
            points.append(list(correct_points))
    print(points)

    ac = execjs.compile(open('get_ac.js', 'r', encoding='utf-8').read()).call('get_ac_click_track', sid, points)
    print(ac)
    data = {
        'ac': ac,
        'ak': ak,
        'c': cc,
        'uid': '',
        'jsv': jsv,
        'sid': sid,
        'aid': aid,
        "type": "3",
        'w': 380,
        'h': 165,
    }
    url = 'https://cap.dingxiang-inc.com/api/v2'
    json_data = s.post(url, headers=headers, data=data).json()
    print(json_data)
    if json_data['success']:
        return True
    else:
        return False


success = 0
for i in range(20):
    retry = 3
    while retry > 0:
        res = run(4)
        if res:
            success += 1
            break
        else:
            retry -= 1
            time.sleep(2)

print(success)
# for i in range(1000):
#     run(4)
# run(4)

# os.makedirs('real_icons', exist_ok=True)
# for i in range(1, 401):
#     url = f'https://static4.dingxiang-inc.com/picture/icon/{i}.png'
#     print(url)
#     with open(f'real_icons/{i}.png', 'wb') as f:
#         f.write(s.get(url).content)
