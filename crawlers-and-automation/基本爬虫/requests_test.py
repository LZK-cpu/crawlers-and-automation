import requests
from lxml import etree
import urllib.request
import ddddocr

url = 'https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/collect.aspx'
base_url = "https://www.gushiwen.cn"

header = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
}

get = requests.get(url=url, headers=header)
tree = etree.HTML(get.text)
VIEWSTATE_names = tree.xpath('//input[@name="__VIEWSTATE"]/@value')
VIEWSTATEGENERATOR_names = tree.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value')

yanzhengma = tree.xpath('//img[@id="imgCode"]/@src')
yzm_url = base_url + yanzhengma[0]
# urllib.request.urlretrieve(url=yzm_url, filename='yzm.jpg')

session = requests.session()
session_get = session.get(yzm_url)
content = session_get.content
with open('yzm.jpg', 'wb') as fp:
    fp.write(content)

ocr = ddddocr.DdddOcr(show_ad=False)
with open('yzm.jpg', 'rb') as fp:
    yzm_img = fp.read()
yzm_code=ocr.classification(yzm_img)

post_url = 'https://www.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fwww.gushiwen.cn%2fuser%2fcollect.aspx'
post_date = {
    '__VIEWSTATE':  VIEWSTATE_names[0],
    '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR_names[0],
    'from': 'http://www.gushiwen.cn/user/collect.aspx',
    'email': '236650137@qq.com',
    'pwd': 'lzk200471',
    'code': yzm_code,
    'denglu': '登录'
}

post = session.post(url=post_url, data=post_date,headers=header)

with open('denglu.html', 'w',encoding='utf-8') as fp:
    fp.write(post.text)


