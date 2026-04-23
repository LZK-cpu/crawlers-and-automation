import datetime
import hashlib
import json
import time

import requests
import execjs

sum_ = 0
for page in range(1, 21):
    timestamp = int(datetime.datetime.now().timestamp() * 1000)
    n = "sssssbbbbb" + str(timestamp)
    ctx = execjs.compile(open('jiami.js', 'r', encoding='utf-8').read())
    s = ctx.call('xxoo', n)
    print(s)
    print(timestamp)
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mashangpa.com/problem-detail/6/",
        "s": s,
        "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "tt": str(timestamp),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    }
    cookies = {
        "sessionid": "aiol7qy3ul1a4ldt6m02t7l0xvo7r2cb",
        "Hm_lvt_0d2227abf9548feda3b9cb6fddee26c0": "1751541472,1751600517",
        "HMACCOUNT": "78A7209821B7C50D",
        "Hm_lpvt_0d2227abf9548feda3b9cb6fddee26c0": "1751603089"
    }
    url = f"https://www.mashangpa.com/api/problem-detail/6/data/?page={page}"
    ctx = execjs.compile(open('jiemi.js', 'r', encoding='utf-8').read())
    response = requests.get(url, headers=headers, cookies=cookies)
    # print(response.text)
    t=json.loads(response.text)['t']
    print(t)
    result = ctx.call('xxxxoooo', t)
    data = json.loads(result)['current_array']
    print(data)
    sum_ += sum(data)
    time.sleep(2)
print(sum_)
