import requests
import json
import openpyxl
from openpyxl.styles import PatternFill, colors
import pandas as pd
import getpass

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
authorizatio = 'Bearer '+login_info['data']['token'] #将Bearer 与token合并成authorizatio

def get_date():
    all_date = [] #存放日期
    starttime = input('输入开始时间：（格式xxxx-xx-xx）')
    endtime = input('输入结束时间：（格式xxxx-xx-xx）')
    date_index = pd.date_range(starttime,endtime) #计算一段时间内的所有日期

    for date in date_index:
        all_date.append(str(date)[:10])   #将所有日期按规定格式存放

    return all_date

def saveall_rank(all_date):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'authorization': authorizatio,
   }
   #只记录登录过程，爬取数据过程省略