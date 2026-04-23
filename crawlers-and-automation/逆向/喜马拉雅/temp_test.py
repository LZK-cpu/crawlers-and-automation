import time

from lxml import etree

import requests
import re
import pdfkit
import execjs

url = 'https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1744875309728?device=www2&trackId=45982775&trackQualityLevel=1'

headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'cookie':
        '_xmLog=h5&0f7d08e1-5205-423e-906c-4260dbd8479a&process.env.sdkVersion; wfp=ACNjMDNmN2IxYzUxMWZiZmYxZn7vaUdr2HZ4bXdlYl93d3c; DATE=1744780412383; crystal=U2FsdGVkX19l2xa7Kwa+xemtPjNThCSaOvk7r4SgPGk1VlEAbYF9KuYtW28gE/Djf0nz4kj2qWWAvG7O403k/vJ15I8gw7CXuF9wTHeRUkNxPlfRzYRmmfXpbHDw+RUtfqA1LzqCoNEo7HRUHBGG4ABirGFEwQeIIg1omfgGro392FOjFyZVy10SnEMOrzRpC+ynMaN3gU2rdl4jP4Lw8VP64MNvik9OUpP8uGmde6jSwiE7LAuaLEqCwfMoiAZC; xm-page-viewid=ximalaya-web; HWWAFSESID=833092359748cf599b2; HWWAFSESTIME=1744853456512; impl=www.ximalaya.com.login; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1744780413,1744808780,1744853499; HMACCOUNT=78A7209821B7C50D; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1744896143; cmci9xde=U2FsdGVkX1/QGOHOt4nRdTB8YwH3sqeXN4t6hTiEYeQNln35Uf7X2dJWSczTfByfq9tBzFOwQRykRa9OLKI13w==; pmck9xge=U2FsdGVkX19Sz1DkQALKmuvurpZJ3mFAsNC47OC5xNk=; assva6=U2FsdGVkX1+uRtLno32SwH+cjx7T/Y31+OaCmTEUDNw=; assva5=U2FsdGVkX19D1sOysgG+9hJbpuVBYTUoX4ge5gjuBj6h+LNQGDbNDQ9rvllSzo/JVNiz4v/UuRKqP7yuVbG86w==; vmce9xdq=U2FsdGVkX1+4mM0ItdFJJvOMRgXibHKXHNvJ+w5helM3AeVE8uWWZtFPjefVSkFyLOEc7Q6O8ZSuBAKe7MVGCbkzfdASlX6UKUeAG6J/U35DDP8wpaRQYuUV/kGNk6ALtZEiDh8HRGNIFk04s+StOxO4KqXH/9HMZai4o6AV2fU=',
    'host':
        'www.ximalaya.com',
    'referer':
        'https://www.ximalaya.com/album/9723091',
    'xm-sign':
        'D2M0y0SXeeDM7ULfCI2FhKxFU47exB8EjB9+vAbhww9VUXf6&&HWHcrD10bem3NuQ39vFQUVvG_qvDhCqAydLVA9Jxf4Y_1'}
get = requests.get(url=url, headers=headers)
data = get.json()
title = data['trackInfo']['title']
mp3_code = data['trackInfo']['playUrlList'][0]['url']
print(f"{title}  {mp3_code}")
jiemi = open('jiemi.js', encoding='utf-8').read()
jiemi_code = execjs.compile(jiemi)
e = {
    "deviceType": "www2",
    "link": mp3_code
}
mp3_url = jiemi_code.call('getSoundCryptLink', e)
print(mp3_url)

with open(f"{title}.mp3", 'wb') as f:
    f.write(requests.get(mp3_url).content)

url = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=9723091&pageNum=1&pageSize=30'
headers={
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'cookie':
        '_xmLog=h5&0f7d08e1-5205-423e-906c-4260dbd8479a&process.env.sdkVersion; wfp=ACNjMDNmN2IxYzUxMWZiZmYxZn7vaUdr2HZ4bXdlYl93d3c; DATE=1744780412383; crystal=U2FsdGVkX19l2xa7Kwa+xemtPjNThCSaOvk7r4SgPGk1VlEAbYF9KuYtW28gE/Djf0nz4kj2qWWAvG7O403k/vJ15I8gw7CXuF9wTHeRUkNxPlfRzYRmmfXpbHDw+RUtfqA1LzqCoNEo7HRUHBGG4ABirGFEwQeIIg1omfgGro392FOjFyZVy10SnEMOrzRpC+ynMaN3gU2rdl4jP4Lw8VP64MNvik9OUpP8uGmde6jSwiE7LAuaLEqCwfMoiAZC; xm-page-viewid=ximalaya-web; HWWAFSESID=833092359748cf599b2; HWWAFSESTIME=1744853456512; impl=www.ximalaya.com.login; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1744780413,1744808780,1744853499; HMACCOUNT=78A7209821B7C50D; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1744898858; cmci9xde=U2FsdGVkX1+PtMciOkBRo4EIiwnxjvu7qvFlywomz6X4I5dx3FF++55Wn4gGV0B9XU07i5jHgVU+pYvbZqO9Rg==; pmck9xge=U2FsdGVkX1+4RNAyOk9rdI3Vtakrr2Cimk8IdIzT7eo=; assva6=U2FsdGVkX1+0868qT1CaWvQWzmyusWY5EcS3l7O0E4Y=; assva5=U2FsdGVkX1/TLFRbnAUGuaH+mnCyTXHevn/EAFBOEi7oCGatk1BpdvSSnbqf3haLVP+PM+yej046dMRsiE7RJg==; vmce9xdq=U2FsdGVkX1+e0CU+ZIr+kpqWAEtOHmE6WL/yKcg52dqx+EQ+4IEU9D/fzvtj3P4TdyPG0j9jGfZ21VWtK0Pbr9hkRwRl1FBlv2bZdHX0M/MHmVYfBe6paG+nmHUa+sb99sNXXxUzcHl4Yg9MUx9/E7Khz6kbU2fUwXfQiukrsWI=',
    'host':
        'www.ximalaya.com',
    'referer':
        'https://www.ximalaya.com/album/9723091',
    'xm-sign':
        'D2M0y0SXeeDM7ULfCI2FhKxFU47exB8EjB9+vAbhww9VUXf6&&FMWubieWRfIY_HIPnp71uYF9DS9IrXbzJFg3m2IAXEI_1'}


get = requests.get(url=url, headers=headers)
data_all=get.json()
tracks_id=[]
for i in range(len(data_all['data']['tracks'])):
    tracks_id.append(data_all['data']['tracks'][i]['trackId'])

print(tracks_id)
print(int(time.time()*1000))