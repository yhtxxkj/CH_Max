#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
新农场卷查询
Author: Joy
Date: 2024年6月28日14:55:51
"""

import time, requests, sys, os, json, random, re, urllib.parse
from datetime import datetime
from functools import partial
print = partial(print, flush=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    from jdCookie import get_cookies
    getCk = get_cookies()
except:
    print("请先下载依赖脚本，\n下载链接: https://raw.githubusercontent.com/HarbourJ/HarbourToulu/main/jdCookie.py")
    sys.exit(3)

def getJdTime():
    jdTime = int(round(time.time() * 1000))
    return jdTime



def superBrandDoTask(ck):
    url = "https://api.m.jd.com/client.action"
    headers = {
        'Cookie': ck,
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://h5.m.jd.com',
        'Referer': 'https://h5.m.jd.com/'
    }
    data = {
    'appid': 'signed_wh5',
    'body': '{"version":3,"type":1}',
    'functionId': 'farm_award_detail',
    }
    response = requests.request("POST", url, headers=headers, data=data)
    res = json.loads(response.text)
    if 'data' in res and 'result' in res['data'] and 'plantAwards' in res['data']['result']:
        first_exchange_remind = res['data']['result']['plantAwards'][0].get('exchangeRemind', '')
        if '有效期至：' in first_exchange_remind:
            try:
                date_str = first_exchange_remind.split('有效期至：')[1].strip()
                expiry_date = datetime.strptime(date_str, '%Y年%m月%d日 %H:%M:%S')
                today = datetime.now()
                if expiry_date > today:
                    match = re.search(r'pt_pin=([^; ]+)', ck)
                    pt_pin_value = match.group(1)
                    UserName = urllib.parse.unquote(pt_pin_value)
                    print("提醒：" + UserName + "|" + first_exchange_remind)
    
            except ValueError:
                print("日期格式错误")
        else:
            print("无兑换卷")   

if __name__ == '__main__':
    try:
        cks = getCk
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()

    num = 0
    for cookie in cks:
        num += 1
        if num % 10 == 0:
            print("⏰等待5s,休息一下")
            time.sleep(5)

        print(f'\n******开始【京东账号{num}】 *********\n')
        try:
            superBrandDoTask(cookie)
        except Exception as e:
            print(e)

        time.sleep(2.1)