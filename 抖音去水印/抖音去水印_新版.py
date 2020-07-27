# coding:utf-8
import re

import requests


def download(url):
    headers = {
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }

    resp = requests.get(url, headers=headers)
    item_id = re.findall("video/(.*?)/\\?", resp.url)[0]
    print("作品id:", item_id)

    api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}".format(item_id)
    resp2 = requests.get(api, headers=headers)
    video_url = resp2.json()["item_list"][0]["video"]["play_addr"]["url_list"][0]
    desc = resp2.json()["item_list"][0]["desc"]  # 获取视频名称
    video_url = re.findall("https.*?&", video_url)[0].replace("&", "").replace('playwm', 'play')
    print("视频链接:", video_url)

    filename = re.sub(r"[/\\:*?\"<>|]", "", desc) + ".mp4"
    with open(filename, "wb") as f:
        resp = requests.get(video_url, headers=headers)
        print("视频链接被重定向到: ", resp.url)
        content = resp.content
        f.write(content)
        print('无水印视频:{}下载成功!!!'.format(filename))


if __name__ == '__main__':
    # "https://v.douyin.com/J1gvdma/"
    download(input("输入抖音链接:"))
