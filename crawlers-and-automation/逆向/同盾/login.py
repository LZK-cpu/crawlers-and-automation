import json
import re
import subprocess
import time

_original_popen = subprocess.Popen


def utf8_popen(*args, **kwargs):
    kwargs['encoding'] = 'utf-8'
    kwargs['errors'] = 'replace'
    return _original_popen(*args, **kwargs)


subprocess.Popen = utf8_popen

import execjs
import base64

from requests import Session

s = Session()
s.verify = False

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://new.hnair.com",
    "Pragma": "no-cache",
    "Referer": "https://new.hnair.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Storage-Access": "active",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://new.hnair.com/hainanair/ibe/common/login.do"
response = s.get(url, headers=headers)

print(s.cookies.get_dict())

match = re.search(r"var\s+ConversationID\s*=\s*'([^']+)'", response.text)
if match:
    conversation_id = match.group(1)
    print(conversation_id)

url = "https://cn-fp.apitd.net/web/profile/v1"
params = {
    "partner": "hainanair",
    "appKey": "0feb1ede51422c358b5666c89cb2b79c"
}

blackbox_data = execjs.compile(open('get_data.js', 'r', encoding='utf-8').read()).call('QoOQoO')
print(blackbox_data)

data = {
    "data": blackbox_data
}
response = s.post(url, headers=headers, params=params, data=data)

json_data = json.loads(response.text)
print(json_data)
requestId = json_data['requestId']
result = json_data['result']
risk_token = execjs.compile(open('get_data.js', 'r', encoding='utf-8').read()).call('Q0QQQo', requestId, result)['tokenId']
print(risk_token)

userName = '19960350272'
password = 'Lzk200471'
password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
url = "https://new.hnair.com/hainanair/ibe/profile/processLoginJSONInRisk.do"
params = {
    "ConversationID": conversation_id
}
headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://new.hnair.com",
    "Pragma": "no-cache",
    "Referer": "https://new.hnair.com/hainanair/ibe/common/login.do",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Storage-Access": "active",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
data = {
    "captcha/verificationType": "ThirdPartyVerification",
    "captcha/verificationCode": "",
    "credentials/loginUsername": userName,
    "credentials/loginPassword": password,
    "RISK_token": risk_token,
    "agreement": "true",
    "loginMethodType": "loginByPwd"
}
res = s.post(url, headers=headers, params=params, data=data)

print(s.cookies.get_dict())

print(res.text.strip())

url = "https://new.hnair.com/hainanair/ibe/common/loginStatus.do"
params = {
    "callback": "jQuery371010432268208915985_" + str(int(time.time() * 1000)),
    "_": str(int(time.time() * 1000) + 1)
}
response = s.get(url, headers=headers, params=params)
print(response.text)
