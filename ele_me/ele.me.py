import requests
import json
import base64
import matplotlib.pyplot as plt
import matplotlib.image as pli

session = requests.session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

mobile = input('输入手机号码：')  #登录号码
data_payload = {
    "mobile":mobile,
    "captcha_value":"",
    "captcha_hash":"",
    "scf":"ms"
    }
ms_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
get_number = session.post(ms_url,headers=headers,data=json.dumps(data_payload))

if get_number.status_code == 400: #获取验证码失败（多次获取验证码会异常），获取图形验证码解异常
    while True: #循环获取验证码直到输对验证码退出循环
        img_url = 'https://h5.ele.me/restapi/eus/v3/captchas'
        data_captcha = {
            "captcha_str":"17382825371"
            }
        get_img = session.post(img_url,headers=headers,data=json.dumps(data_captcha))
        img_info = json.loads(get_img.text)
        img = img_info['captcha_image'][23:] #（[23:]）一定要去掉data:image/jpg:base64,。切记切记
        img = base64.b64decode(img)
        fh = open("pic.jpg","wb")
        fh.write(img)
        fh.close()
        image = plt.imread('pic.jpg')    #输入图片路径，如果是在当前工作路径下可以只写xx.jpg
        plt.imshow(image)
        plt.show()  #打开验证码图片

        login_info = json.loads(get_img.text)
        captcha_hash = login_info['captcha_hash']
        code = input('输入图形验证码：')
        data_img = {
            "mobile":"17382825371",
            "captcha_value":code,
            "captcha_hash":captcha_hash,
            "scf":"ms"
            }
        url_code = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
        put_code = session.post(url_code,headers=headers,data=json.dumps(data_img))
        if put_code.status_code == 200:
            login_info = json.loads(put_code.text)
            validate_token = login_info['validate_token'] #如果需要输入图形验证码，那么需要重从提交图形验证码处获取validate_token
            break
else:
    login_info = json.loads(get_number.text)
    validate_token = login_info['validate_token'] #无异常正常获取validate_token

number = input('输入短信验证码：')
data_payload1 = {"mobile":"17382825371","validate_code":number,"validate_token":validate_token,"scf":"ms"}

login_url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
login = session.post(login_url,headers=headers,data=json.dumps(data_payload1))
if login.status_code == 200:
    print('登录成功')