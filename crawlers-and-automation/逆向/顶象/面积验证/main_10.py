import random
import time

import cv2
import execjs
import numpy as np
from requests import Session

from type_ak import appId_dict

s = Session()
s.verify = False


def get_max_area(content):
    img_array = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

    max_area = 0
    max_label = 0

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > max_area:
            max_area = area
            max_label = i

    mask = (labels == max_label).astype(np.uint8) * 255

    cx, cy = centroids[max_label]
    cx, cy = int(cx), int(cy)

    result = img.copy()

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(result, contours, -1, (0, 0, 255), 2)

    cv2.circle(result, (cx, cy), 5, (0, 0, 255), -1)

    print(cx, cy)
    return [int(cx / 300 * 380), int(cy / 150 * 165)]


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
    tp = url_a_res['tp1']
    image = 'https://static4.dingxiang-inc.com/picture' + tp
    content = s.get(image).content
    point = get_max_area(content)
    ac = execjs.compile(open('get_ac.js', 'r', encoding='utf-8').read()).call('get_ac_one_click', sid, point)
    print(ac)

    url = "https://cap.dingxiang-inc.com/api/v2"
    data = {
        "ac": ac,
        "ak": ak,
        "c": cc,
        "jsv": jsv,
        "sid": sid,
        "aid": ak,
        "uid": "",
        "type": "8",
        "w": "380",
        "h": "165"
    }
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
        res = run(10)
        if res:
            success += 1
            break
        else:
            retry -= 1
            time.sleep(2)

print("success:", success)
