import base64

import ddddocr
import requests
import json
import execjs


def get_params(data):
    params = (execjs.compile(open('jiami.js', encoding='utf-8').read())).call('jiemi', data)
    print(params)
    return params

count=0
for i in range(100):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://ynjzjgcx.com",
        "Pragma": "no-cache",
        "Referer": "https://ynjzjgcx.com/dataPub/enterprise",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "appId": "84ded2cd478642b2",
        "isToken": "false",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    imagre_url = "https://ynjzjgcx.com/prod-api/mohurd-pub/vcode/genVcode"
    image_data = {"key": "query"}
    data = {
        "params":
            get_params(image_data)
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(imagre_url, headers=headers, data=data)

    print(response)

    base64_string_small = json.loads(json.loads(response.text)['data'])['smallImage']
    base64_string_big = json.loads(json.loads(response.text)['data'])['bigImage']
    slideid = json.loads(json.loads(response.text)['data'])['slideId']
    smallimage_data = base64.b64decode(base64_string_small)
    bigimage_data = base64.b64decode(base64_string_big)
    print(slideid)
    with open("small_image.png", "wb") as f:
        f.write(smallimage_data)
    with open("big_image.png", "wb") as f:
        f.write(bigimage_data)

    ocr = ddddocr.DdddOcr(show_ad=False, det=False, ocr=False)
    with open('small_image.png', 'rb') as f:
        small_data = f.read()
    with open('big_image.png', 'rb') as f:
        big_data = f.read()
    res = ocr.slide_match(small_data, big_data, simple_target=True)
    wigth = res['target'][0]
    print(wigth)
    content_url = 'https://ynjzjgcx.com/prod-api/mohurd-pub/dataServ/findBaseEntDpPage'
    content_data = {
        "pageNum": 1,
        "pageSize": 10,
        "certificateType": "",
        "name": "",
        "slideId": str(slideid),
        "key": "query",
        "width": wigth
    }
    data = {
        "params":
            get_params(content_data)
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(content_url, headers=headers, data=data)
    print(response.text)
    if json.loads(response.text)['msg']:
        count+=1

print(count)