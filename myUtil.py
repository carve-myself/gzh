# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import os
import os.path
import re
import shutil
import time
import traceback
from configparser import ConfigParser

import requests
from lxml import etree

# region ---------------------       常量        -------------------------
UTF8 = "utf-8"
# endregion


# region ---------------------       网络请求        -------------------------
default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}


# 获取html
def get_html(url, headers=None):
    return get_resp(url, headers).text


# 获取requests
def get_resp(url, headers=None):
    if headers is None:
        headers = default_headers
    return requests.get(url, headers=headers)


# 保存文件,图片,视频等二进制流
def save_file_with_url(url, filename, headers=None):
    with open(filename, "wb") as f:
        f.write(get_resp(url, headers).content)
    print("文件 {} 保存成功!".format(filename))


# 保存文本,网页
def save_text_with_url(url, filename, headers=None):
    with open(filename, "w", encoding=UTF8) as f:
        f.write(get_resp(url, headers).text)
    print("文件 {} 保存成功!".format(filename))


# endregion


# region ---------------------       文件操作        -------------------------

# 合并一个文件夹下多个文件
def merge_files(directory_path, outfilePath):
    """ directory_path: 文件夹目录           outfilePath: 输出文件路径,包括文件名 """
    with open(outfilePath, 'a+', encoding=UTF8) as of:
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
        # 所以root+file = 目录下每一个文件路径
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, encoding=UTF8) as f:
                    # 换行写入
                    of.write(f.read() + "\n")
    print("合并完成")


# 删除文件夹下的空目录
def remove_empty_dir(path):
    for root, dirs, files in os.walk(path):
        for item in dirs:
            dir_path = os.path.join(root, item)
            try:
                os.rmdir(dir_path)
                print("删除空目录", dir_path.replace("\\", "/"))
            except:
                pass


# 追加内容到文件头部
def append_head_file(file_path, content):
    """ file_path: 文件路径         content: 追加的内容 """
    with open(file_path, 'r+', encoding=UTF8) as f:
        old = f.read()
        f.seek(0)
        f.write(content)
        f.write(old)
        print("追加到头部成功")


# 图片格式转换
def imgConvert(input_path, out_path, remove_input_file=False):
    """
    已测试的格式 jpg gif png bmp jpeg
    :param input_path: 原图路径
    :param out_path:  保存位置
    :param remove_input_file:
    """
    from PIL import Image
    to_gif = Image.open(input_path)
    to_gif.save(out_path)

    # 删除原图
    if remove_input_file:
        os.remove(input_path)
        print("原文件删除成功")
    print("图片已转为:", out_path)


# 获取配置文件对象
def read_config(ini_file):
    cfg = ConfigParser()
    cfg.read(ini_file, encoding=UTF8)
    return cfg


# 读取文件
def read_file(src):
    with open(src, "r", encoding=UTF8) as f:
        return f.read()


# m3u文件追加,无文件则创建
def append_m3u8(file_path, img_url, group_name, video_name, video_url):
    """ file_path 如 1.m3u """
    content = '#EXTINF:-1 tvg-logo="{}" group-title="{}", {}\n{}\n\n'.format(img_url, group_name, video_name, video_url)
    if not os.path.exists(file_path):
        content = "#EXTM3U\n" + content
    with open(file_path, mode="a", encoding=UTF8) as f:
        f.write(content)


# 保存文本文件
def save_text(filename, text):
    with open(filename, "w", encoding=UTF8) as f:
        f.write(text)
    print("文件 {} 保存成功!".format(filename))


# 保存二进制文件
def save_file(filename, content):
    with open(filename, "wb") as f:
        f.write(content)
    print("文件 {} 保存成功!".format(filename))


# endregion


# region ---------------------       文本解析处理        -------------------------

# 正则匹配返回所有
def findall(re_str, text):
    return re.findall(re_str, text)


# 正则匹配返回第一个
def findOne(re_str, text):
    return findall(re_str, text)[0]


# 格式化字符串
def checkText(text):
    return re.sub("[/\\\:*?\"<>|]", "_", text)


# 获取xpath对象
def get_xpath(html_str):
    return etree.HTML(html_str)


# endregion


# region ---------------------       json        -------------------------
# json字符串转对象
def json2obj(text):
    return json.loads(text)


# 对象转json字符串
def obj2json(obj, indent=2):
    return json.dumps(obj, ensure_ascii=False, indent=indent)


# 将json文件转成对象
def read_file_json(src):
    with open(src, "r", encoding=UTF8) as f:
        return json2obj(f.read())


# endregion


# region ---------------------       其它        -------------------------

# 生成指定范围的日期
def dateRange(beginDate, endDate, split_str):
    """ beginDate: '2020/01/01'     endDate: '2020/01/08'  split_str: '/' """
    dates = []
    format_str = "%Y{}%m{}%d".format(split_str, split_str)
    dt = datetime.datetime.strptime(beginDate, format_str)
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime(format_str)
    return dates


# 打印异常信息
def print_exc():
    traceback.print_exc()


# md5加密
def md5(text):
    m = hashlib.md5()
    m.update(text.encode('UTF-8'))
    return m.hexdigest()


# 执行cmd命令
def cmd(command):
    os.system(command)


# 获取时间戳 毫秒级 长度13
def get_timestamp():
    return str(int(time.time() * 1000))


# 输出调试
def debug(*obj):
    print('\033[1;46m', *obj, '\033[0m')


# endregion

if __name__ == '__main__':
    src = "myUtil.py"
    dic = "C:/Users/Administrator/AppData/Local/Programs/Python/Python38/Lib/site-packages"
    shutil.copy(src, dic)
    print("部署成功")
