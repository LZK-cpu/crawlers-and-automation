import random
import time
from io import BytesIO

import cv2
import ddddocr
import execjs
import numpy as np
from requests import Session
from PIL import Image
from type_ak import appId_dict

ocr = ddddocr.DdddOcr(show_ad=False, det=False, beta=True)
s = Session()
s.verify = False


def arr(r):
    t = []
    for n in range(len(r)):
        e = ord(r[n])
        if 32 == n:
            break
        while e % 32 in t:
            e += 1
        t.append(e % 32)
    return t + [32]


def img_recover(location_array, img_url, shape):
    w = shape[0]
    h = shape[1]
    img = np.array(Image.open(
        BytesIO(s.get(url=img_url, verify=False).content)))
    new_img = np.zeros((h, w, 3), dtype=np.uint8)
    lk = len(location_array)
    ck = int(w / lk)
    for cp in range(lk):
        c = location_array[cp] % lk * ck
        xp = cp % lk * ck
        slice_img = img[0: h, c: c + ck]
        new_img[0: h, xp:xp + len(slice_img[0])] = slice_img
    return new_img


def get_distance(tg_byte, bg_bytes):
    bg_img = cv2.imdecode(np.frombuffer(bg_bytes, np.uint8), cv2.IMREAD_COLOR)
    tg_img = cv2.imdecode(np.frombuffer(tg_byte, np.uint8), cv2.IMREAD_UNCHANGED)
    if len(tg_img.shape) == 3 and tg_img.shape[2] == 4:
        tg_img = cv2.cvtColor(tg_img, cv2.COLOR_BGRA2BGR)

    bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    tg_gray = cv2.cvtColor(tg_img, cv2.COLOR_BGR2GRAY)
    tg_gray = abs(255 - tg_gray)

    result = cv2.matchTemplate(bg_gray, tg_gray, cv2.TM_CCOEFF_NORMED)

    _, _, _, max_loc = cv2.minMaxLoc(result)

    x, y = max_loc

    return x


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
    cc = "69cf6f6byRl5ga18qNcqcnxeFRedZvnJiKGsiPJ1"
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
    ay = str(url_a_res.get("y"))
    p1 = url_a_res.get("p1")
    p2 = url_a_res.get("p2")

    image_p1 = "https://static.dingxiang-inc.com/picture" + p1
    image_p2 = "https://static.dingxiang-inc.com/picture" + p2

    p1_arr = arr(p1.split('.')[0].split('/')[-1])
    recover_p1 = img_recover(p1_arr, image_p1, [400, 200])
    _, bg_bytes = cv2.imencode('.png', recover_p1)
    bg_bytes = bg_bytes.tobytes()

    tg_bytes = s.get(image_p2).content
    distance = get_distance(tg_bytes, bg_bytes)
    print(distance)
    distance = str(int(distance) - 10)

    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.dingxiang-inc.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.dingxiang-inc.com/",
        "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Microsoft Edge\";v=\"146\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
    }

    x_distance, y_distance = int(distance), int(ay)
    ac = execjs.compile(open('get_ac.js', 'r', encoding='utf-8').read()).call('get_ac_slide', sid, None, [int(x_distance), int(y_distance)])
    print(ac)

    data = {
        'ac': ac,
        'ak': ak,
        'c': cc,
        'uid': '',
        'jsv': jsv,
        'sid': sid,
        'code': '',
        'aid': aid,
        'x': x_distance,
        'y': y_distance,
        'w': 380,
        'h': 165,
    }
    url = 'https://cap.dingxiang-inc.com/api/v1'
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
        res = run(2)
        if res:
            success += 1
            break
        else:
            retry -= 1
            time.sleep(2)

print("success:", success)
