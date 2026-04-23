import base64
import json
import warnings
from datetime import datetime

import execjs
from Crypto.Cipher import DES
from loguru import logger
from requests import Session

warnings.filterwarnings('ignore')
from threading import Lock

import time

lock = Lock()
import random

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'


def search_flight(session, ua):
    headers = {
        'Host': 'www.shenzhenair.com',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.shenzhenair.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,images/avif,images/webp,images/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.shenzhenair.com/szair_B2C/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'hcType': 'DC',
        'type': '单程',
        'orgCity': '北京大兴',
        'orgCityCode': 'PKX',
        'dstCity': '广州',
        'dstCityCode': 'CAN',
        'orgDate': '2026-02-26',
        'dstDate': '2026-02-26',
        'quiz': [
            'Y',
            '1',
        ],
        'bzcPsgrName': '',
        'bzcCertNo': '',
    }
    response = session.post('https://www.shenzhenair.com/szair_B2C/flightsearch.action', headers=headers, data=data)
    if response.status_code == 200:
        logger.info('成功')
        logger.info(response.cookies)
        logger.info(session.cookies.get_dict())
        headers = {
            'Host': 'www.shenzhenair.com',
            'sec-ch-ua-platform': '"Windows"',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': ua,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'sec-ch-ua-mobile': '?0',
            'Origin': 'https://www.shenzhenair.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.shenzhenair.com/szair_B2C/flightsearch.action',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'JSESSIONID=E4507A3B2F4E6531A59D4CE677D92D84; HMF_CI=98df2d903c72ffbb69a6f92607fa4e6d651724bb9fc9acb67134f098dbc355309dbc01d3b194461f7f431d48bb22198ea824ff1dda523bc991a3a8dcf38baf4067; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219ac15e102f1f51-0d5b712d3eaf9a8-26061b51-2073600-19ac15e10301086%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219ac15e102f1f51-0d5b712d3eaf9a8-26061b51-2073600-19ac15e10301086%22%7D; x-s3-sid=S1esvxxhmrRte34413lm9bazc; arialoadData=false; sw_rtk=WW313lm9baitKn3l6tR9e3447b3e; x-s3-s4e=Bo2DHNxUY6bQlAZQBbDuThn9oQ7Zrmwyrc3ZAnFpw60292lyW8W1I19178V8nxl25Nv0rSdpg16WBWuwvX1NAX3EsQXlAGTUytVGcI0LSChxPE5sDBex83D6bfPidTgD6Za39gRDXfmLe2bd0WoYuYMR7mEQGvXsCXg6u%2BUO2AaY06OilVwg2r6wiQtLevgIi%2BDsmvB3mSlNOS3p8sevw8HDjBXEHnNFcRoJz8dOybQkTPotHS5eyuJe%2BclDkTt9jZOXda%2Fj0u1GMoObwaiNNlsRyQUEOrNsyycaMdfdyuJXR3A8JS0Bk5rWNRbnSM9rF%2BJeEtDMOt4CJxqkOgl2iL5E3MJxN%2BnpnP4LClK%2Fn6%2FObVcJDWhImx80%2FrX1wH8JgYLap90SiJf%2F366YRHPvDEweg%2Bzx%2FgkD7kI9iYEhMT%2BLy2caMxD541msenlz65mUilcXQlGmuCiPlABaaqcztI%2FJATQpdcqunvFYh03vugmH9cLf2hOCB%2BFgkZ9%2FRzG5Nu25wf6Swgz7q9sAM1F1iIuE7q7HyC7qpxKZrEaw9g2mIOXopUxECP9w7wNsJxNMilcXQlGmuCiPlABaaqcztPHq5geRKkLTbepE9x5mC98xmIan92e%2B%2BLUpxDSc43eGmrwbTEeHRpCU08QqcYG4mGVlK0YaRK10j1itjU7R7eWHjyAFuNaXwO9e213SJfd8DKdyFeLADQcEtP%2Bh5%2B4BU2UetIGgiTQY3adcjGMGcVCvFsyO6h704FHjHGqgByfJ%2FekbHT1OHbBJUp5zt8tmKcrwwftiZlM8bChL0ELF7JfOFLDPDlGmV1NToUZMRwilEU71wsOXUdjZuhDzPTR6JA%3D%3D3sSsc843cbca809d97273a47bb0accda6059c8d15610:48:19408e6e-cbaf-11f0-a33d-3cd2e55daed6:0020402094; x-s3-tid=c843cbca809d97273a47bb0accda6059c8d15610:48:19408e6e-cbaf-11f0-a33d-3cd2e55daed6:0020402094; fromPage=%7BfromPage%3A%22index%22%7D; sccode=%7BsccodeInfo%3A%22%u9996%u9875%26%22%7D; AlteonP=ACBHUW9ADgr+ZtsB4r5DNg' + os.getenv('$', '') + '; ariauseGraymode=false',
        }
        data = {
            'condition.orgCityCode': 'PXK',
            'condition.dstCityCode': 'CAN',
            'condition.hcType': 'DC',
            'condition.orgDate': '2026-02-26',
            'condition.dstDate': '2026-02-26',
        }
        response = session.post('https://www.shenzhenair.com/szair_B2C/flightSearch.action', headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
            # return True
    else:
        logger.info(response.status_code)
        logger.info(response.text)


context = execjs.compile(open('get_x_s3_s4e.js', 'r', encoding='utf-8').read())


def get_cookie(session, ip, ua, key, fp, fcp, cvp):
    s = session
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,images/avif,images/webp,images/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    r = s.get('https://www.shenzhenair.com/szair_B2C/', headers=headers)
    print(s.cookies)
    headers_js = {

        'Host': 'www.shenzhenair.com',
        'sec-ch-ua-platform': '"Windows"',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': ua,
        'Accept': '*/*',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://www.shenzhenair.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.shenzhenair.com/szair_B2C/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://www.shenzhenair.com/szair_B2C/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": ua,

    }
    url = "https://www.shenzhenair.com/vodka/v1/bootstrap/param"
    ts = int(time.time() * 1000)
    params = {
        "t": ts
    }
    response = s.get(url, headers=headers, params=params)
    data_json = json.loads(response.text)
    x_s3_tid = data_json['_a'][0]
    x_s3_sid = data_json['_a'][1]
    headers = {
        'Host': 'www.shenzhenair.com',
        'sec-ch-ua-platform': '"Windows"',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://www.shenzhenair.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.shenzhenair.com/szair_B2C/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    url = "https://www.shenzhenair.com/szair_B2C/floorConfig/queryFloorConfigDetail.action"
    for i in range(2):
        params = {
            "configModule": "1"
        }
        r = s.get(url, headers=headers, params=params)

    # response = s.post('https://www.shenzhenair.com/szair_B2C/login/loginInformation.action',headers=headers)
    # response = s.post('https://www.shenzhenair.com/szair_B2C/login/loginInformation.action', headers=headers)
    with lock:
        data = context.call('get_x_s3_s4e', x_s3_tid, x_s3_sid, ip, ua, key, fp, fcp, cvp)
    x_s3_s4e = data['x_s3_s4e']
    s.cookies.set('x-s3-s4e', x_s3_s4e, domain='.shenzhenair.com', path='/')
    s.cookies.set('x-s3-tid', x_s3_tid, domain='.shenzhenair.com', path='/')
    logger.info(s.cookies.get_dict())


def test():
    alnum = 'abcdefghijklmnopqrstuvwxyz0123456789'
    fcp = ''
    cvp = ''
    for i in range(8):
        index1 = random.randint(0, len(alnum) - 1)
        fcp += alnum[index1]
        index2 = random.randint(0, len(alnum) - 1)
        cvp += alnum[index2]
    logger.info(fcp + ' ' + cvp)
    s = Session()
    s.trust_env = False
    proxy = s.get(
        'http://api.tianqiip.com/getip?secret=u4kncdfw&num=1&type=txt&port=1&mr=1&sign=91ac51fd3232c447486480bcb89d831f',
        proxies=None).text.strip()
    print(proxy)
    ip_port = proxy.split(':')
    ip = ip_port[0]
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    # s.proxies = proxies
    s.allow_redirects = True
    s.verify = False

    get_cookie(s, ip, useragent, None, None, fcp, cvp)
    r = search_flight(s, useragent)
    print(r)
    return r



result = test()
# print(result)
