import requests
import json
import getpass
import csv
import os

def login():
    try:
        if os.path.exists('authorization.csv'):
            with open('authorization.csv','r',encoding='utf-8') as f:
                reader = csv.reader(f)
                for i in reader:
                    authorization = i[0]
                    break
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'authorization': authorization,
        }
        info_url = 'https://prod.pandateacher.com/ninth-studio/api-ai-boss/python/admin/info'
        info = requests.get(info_url,headers=headers)
        info = info.json()
        print(info['data']['name']+'，你好')
        return authorization
    except Exception as e:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }

        while True:
            username = input('请输入登录帐号（手机号）：')
            password = getpass.getpass('请输入密码（密码不可见）：')
            payloadData = {"username":username,"password":password}  #payload形式的请求
            login_url = 'https://prod.pandateacher.com/ninth-studio/api-ai-boss-go/login'
            login = requests.post(login_url,headers=headers,data=json.dumps(payloadData)) #其他形式的POST请求，是放到 Request payload 中（现在是为了方便阅读，使用了Json这样的数据格式），请求的Content-Type设置为application/json;charset=UTF-8或者不指定。
            if login.status_code == 200:
                print('登录成功')
                break
            else:
                print('\033[1;31m帐号或密码输入错误,请重新输入\033[0m')

        login_info = json.loads(login.text) #将保存的login转成字典
        authorization = 'Bearer '+login_info['data']['token'] #将Bearer 与token合并成authorization

        with open('authorization.csv','w',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([authorization])
        return authorization
