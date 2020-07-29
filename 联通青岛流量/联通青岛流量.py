import sys
import time

import requests


def send(phone):
    data1 = {'phoneVal': phone, 'type': '21'}
    resp = requests.post('https://m.10010.com/god/AirCheckMessage/sendCaptcha', data=data1)
    print("发送请求:", resp.text)

    if '一天最多只能发送三次' in resp.json().get("RespMsg", ""):
        print('今天已经领完啦！请明天再来吧。')
        print("10s后退出...")
        time.sleep(10)
        sys.exit(1)

    code = input('手机验证码:').strip()
    code_url = 'https://m.10010.com/god/qingPiCard/flowExchange?number={}&type=21&captcha={}'.format(phone, code)
    resp2 = requests.get(code_url)
    print("结果:", resp2.text)


def run():
    phone = input('请输入你的手机号：')
    for i in range(3):
        send(phone)
        print('剩余次数:{}; 60秒后进行发送'.format(2 - i))
        time.sleep(60)

# https://wwe.lanzous.com/i27fAf0v0ub
run()
