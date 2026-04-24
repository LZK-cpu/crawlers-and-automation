import random
import time
from io import BytesIO

import cv2
import execjs
import numpy as np
from PIL import Image
from requests import Session
from type_ak import appId_dict
from wff_diff import process_chinese_diff

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
    aid = 'dx-{}-27682978-3'.format(str(int(ts * 1000)))
    ak = appId_dict[type]
    cc = "6554343aU0MT73yU0M2yQGgeDMa2Xtr12D7gEwc1"
    cid = "05592352"
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
    image_p1 = "https://static.dingxiang-inc.com/picture" + tp
    p1_arr = arr(tp.split('.')[0].split('/')[-1])
    recover_p1 = img_recover(p1_arr, image_p1, [330, 165])
    cv2.imwrite('img.png', recover_p1)
    point = process_chinese_diff(recover_p1)
    print(point)
    ac = execjs.compile(open('get_ac.js', 'r', encoding='utf-8').read()).call('get_ac_one_click', sid, point)
    print(ac)
    url = "https://cap.dingxiang-inc.com/api/v2"
    data = {
        "ac": ac,
        "ak": ak,
        "c": cc,
        "jsv": jsv,
        "sid": sid,
        "aid": aid,
        "uid": "",
        "type": "12",
        "w": "380",
        "h": "165"
    }
    res = s.post(url=url, headers=headers, data=data).json()
    print(res)

success = 0
for i in range(20):
    retry = 3
    while retry > 0:
        res = run(13)
        if res:
            success+=1
            break
        else:
            retry-=1
            time.sleep(2)

print("success:", success)
# run(13)
