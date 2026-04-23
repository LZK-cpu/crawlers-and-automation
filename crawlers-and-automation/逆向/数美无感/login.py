import time
import json
import base64
from concurrent.futures import ThreadPoolExecutor

from loguru import logger
from lxml import etree
from requests import Session
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

sign_js_code = execjs.compile(open('get_sign.js', 'r', encoding='utf-8').read())
device_js_code = execjs.compile(open('get_device_id.js', 'r', encoding='utf-8').read())
fp_js_code = execjs.compile(open('get_fp.js', 'r', encoding='utf-8').read())

s = Session()
s.verify = False

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"


def rsa_encrypt(message, rsa_publicKey):
    rsa_publicKey = pem_key = f"-----BEGIN PUBLIC KEY-----\n{rsa_publicKey}\n-----END PUBLIC KEY-----"
    key = RSA.import_key(rsa_publicKey)
    cipher = PKCS1_v1_5.new(key)
    encrypted = cipher.encrypt(message.encode('utf-8'))
    return base64.b64encode(encrypted).decode()


def login():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,images/avif,images/webp,images/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.airjiangxi.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": userAgent,
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://ecipuia.xiamenair.com/api/v1/oauth2/authorize"
    params = {
        "uia_type": "st",
        "client_id": "ry_client",
        "lang": "zh-cn",
        "redirect_uri": "https://www.airjiangxi.com/jiangxiair/user/loginRedirect.action"
    }
    response = s.get(url, headers=headers, params=params)

    organization_pattern = r"organization\s*:\s*'([^']+)'"
    organization = re.search(organization_pattern, response.text).group(1)
    logger.info('organization ' + organization)
    pageToken = etree.HTML(response.text).xpath('//input[@class="pageToken"]/@value')[0]
    logger.info('pageToken ' + pageToken)
    clientId = etree.HTML(response.text).xpath('//input[@class="clientId"]/@value')[0]
    logger.info('clientId ' + clientId)

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Pragma": "no-cache",
        "Referer": "https://ecipuia.xiamenair.com/api/v1/oauth2/authorize?uia_type=st&client_id=ry_client&lang=zh-cn&redirect_uri=https%3A%2F%2Fwww.airjiangxi.com%2Fjiangxiair%2Fuser%2FloginRedirect.action",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": userAgent,
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://ecipuia.xiamenair.com/api/v1/oauth2/getPublicKey"
    response = s.get(url, headers=headers)
    json_data = json.loads(response.text)
    logger.info(json_data)
    publicKey = json_data['result']['publicKey']
    keyPairId = json_data['result']['keyPairId']
    logger.info('publicKey ' + publicKey)
    logger.info('keyPairId ' + keyPairId)

    account = rsa_encrypt("自己的账号", publicKey)
    logger.info('account ' + account)
    password = rsa_encrypt("自己的密码", publicKey)
    logger.info('password ' + password)

    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "origin": "https://ecipuia.xiamenair.com",
        "pragma": "no-cache",
        "referer": "https://ecipuia.xiamenair.com/",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    ts = str(int(time.time() * 1000))
    logger.info(ts)
    smdata = sign_js_code.call('get_smdata')
    logger.info('smdata ' + smdata)
    url = "https://fp-it.portal101.cn/v3/profile/web"
    params = {
        "callback": "smCB_" + ts,
        "organization": organization,
        "smdata": smdata,
        "os": "web",
        "version": "2.0.0",
        "_": ts
    }
    response = s.get(url, headers=headers, params=params)

    json_data = json.loads(response.text.split('(')[1].split(')')[0])
    logger.info(json_data)
    sign = json_data['detail']['sign']
    timestamp = json_data['detail']['timestamp']
    length = json_data['detail']['len']
    logger.info('sign ' + sign)
    logger.info(timestamp)
    logger.info(length)

    fp = fp_js_code.call('get_fp')
    logger.info('fp ' + fp)

    device_id = device_js_code.call('get_device_id', userAgent, sign, timestamp, length)
    logger.info('device_id ' + device_id)

    url = "https://ecipuia.xiamenair.com/api/v1/oauth2/verify"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://ecipuia.xiamenair.com",
        "Pragma": "no-cache",
        "Referer": "https://ecipuia.xiamenair.com/api/v1/oauth2/authorize?uia_type=st&client_id=ry_client&lang=zh-cn&redirect_uri=https%3A%2F%2Fwww.airjiangxi.com%2Fjiangxiair%2Fv2%2Findex.action",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    data = {
        "pageToken": pageToken,
        "account": account,
        "password": password,
        "type": "1",
        "deviceId": fp,
        "clientId": clientId,
        "uiaType": "st",
        "state": "",
        "promotionId": "",
        "smDeviceId": device_id,
        "keyPairId": keyPairId
    }
    data = json.dumps(data, separators=(',', ':'))
    response = s.post(url, headers=headers, data=data)
    logger.info(response.status_code)
    logger.info(response.text)
    json_data = json.loads(response.text)
    redirectUrl = json_data['result']['redirectUrl']
    logger.info(redirectUrl)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,images/avif,images/webp,images/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://ecipuia.xiamenair.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    response = s.get(redirectUrl, headers=headers)
    login_name = etree.HTML(response.text).xpath('//div[@class="log-in-after"]/span/em/text()')[0]
    logger.info(login_name)

login()

