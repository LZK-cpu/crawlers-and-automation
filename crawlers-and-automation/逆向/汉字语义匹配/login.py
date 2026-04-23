import base64
import hashlib
import os
import time
from io import BytesIO

from PIL import Image
from requests import Session
import json

from GS.ch_ocr import get_mfamate

s = Session()
s.verify = False

headers = {
    "Accept": "application/json",
    "Accept-Language": "zh-CN",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "IP-Address": "1.1.1.1",
    "Origin": "https://www.tianjin-air.com",
    "Pragma": "no-cache",
    "Referer": "https://www.tianjin-air.com/",
    "Sales-Channel": "IBE",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Tenant": "GS",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


index=0

success = 0
start = time.time()
for j in range(20):
    s.cookies.clear()
    for i in range(3):
        if 'Mfa-Mate' in headers:
            headers.pop('Mfa-Mate')
        url = "https://www.tianjin-air.com/air/api/uc/v1/profile/profile/authenticaiton/captchas"
        data = {
            "authenticationType": "THIRD_PARTY"
        }
        data = json.dumps(data, separators=(',', ':'))
        response = s.post(url, headers=headers, data=data)
        json_data = json.loads(response.text)
        captchaId = json_data['captchaId']
        question_content = json_data['questionImage']['content']
        q_img_hash = hashlib.sha256(question_content.encode()).hexdigest()
        img_data = base64.b64decode(question_content)
        img = Image.open(BytesIO(img_data))
        img.save('question.png', "PNG")
        answerImageList = json_data['answerImageList']
        for answerImage in answerImageList:
            answerImage_id = answerImage['id']
            answerImage_content = answerImage['content']
            img_data = base64.b64decode(answerImage_content)
            img = Image.open(BytesIO(img_data))
            img.save(f'./testImage/{answerImage_id}.png', "PNG")
            index+=1
        answer = get_mfamate()
        print(answer)
        url = "https://www.tianjin-air.com/air/api/uc/v1/user/ffp/login"
        data = {
            "number": "19960350272",
            "password": "THprMjAwNDcx"
        }
        data = json.dumps(data, separators=(',', ':'))
        mfamate = {
            "captcha": {
                "id": captchaId,
                "answers": answer
            }
        }
        mfamate = json.dumps(mfamate, separators=(',', ':'))
        headers.update({"Mfa-Mate": mfamate})
        response = s.post(url, headers=headers, data=data)
        print(response.text)
        if response.status_code == 200:
            break
        os.remove('question.png')
    url = "https://www.tianjin-air.com/air/api/uc/v1/profile/profile_view"
    data = {
        "isIncludeMemberInfo": "Y",
        "isIncludeAccountsInfo": "Y",
        "isIncludeRelationPassenger": "Y"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = s.post(url, headers=headers, data=data)
    json_data = json.loads(response.text).get('memberInfo')
    if json_data:
        success+=1

end = time.time()
print('登录成功率'+str(success/20*100)+'%')
print('平均耗时'+str((end-start)/20)+'s')