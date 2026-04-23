import requests
import execjs

for page in range(1,7):
    js_a=execjs.compile(open('jiami_a.js',encoding='utf-8').read())
    a=js_a.call('get_a',page)
    js_jiami=execjs.compile(open('jiami.js', encoding='utf-8').read())
    code=js_jiami.call('encode',a)


    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/xml;charset=UTF-8",
        "Origin": "https://ccprec.com",
        "Pragma": "no-cache",
        "Referer": "https://ccprec.com/projectSecPage/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://ccprec.com/honsanCloudAct"
    data = (
        code
        .encode('unicode_escape'))
    response = requests.post(url, headers=headers, data=data)

    print(response.text)

    content_js = execjs.compile(open('jiemi.js', encoding='utf-8').read())
    content=content_js.call('decode',response.text)
    print(content)