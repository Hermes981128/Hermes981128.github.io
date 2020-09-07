# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：personal_web_page -> check_password
@IDE    ：PyCharm
@Author ：Hermes
@Date   ：2020/8/15 20:15
@Desc   ：
=================================================='''
import logging, re,base64,requests,random,time,json
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from sys import version_info
from urllib import parse

def login(username,password):
    def check_result():
        url='http://my.nuist.edu.cn/index.portal'
        response=session.get(url)
        if '欢迎您' in response.text:
            print('登陆成功')
            # print(response.text)
            return True
        else:
            print('登陆失败')
            return False
            # print(response.text)
    def get_cookie():
        CASTGC = requests.utils.dict_from_cookiejar(session.cookies)['CASTGC']
        url='http://my.nuist.edu.cn/index.portal?ticket={}'.format(CASTGC)
        session.get(url)
    def base64_api(img,uname="Hermes981128", pwd="wang720521"):
        img = img.convert('RGB')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        if version_info.major >= 3:
            b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
        else:
            b64 = str(base64.b64encode(buffered.getvalue()))
        data = {"username": uname, "password": pwd, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            print(result["data"]["result"])
            return result["data"]["result"]
        else:
            return result["message"]
        return False

    def get_captcha():
        url='http://authserver.nuist.edu.cn/authserver/getCaptcha.htl?1597757330522'
        response=session.get(url)
        response_byte = response.content
        bytes_stream = BytesIO(response_byte)
        capture_img = Image.open(bytes_stream)
        return base64_api(img=capture_img)

    def checkNeedCaptcha(username):
        url="http://authserver.nuist.edu.cn/authserver/checkNeedCaptcha.htl?username={}&_={}".format(username,int(time.time()))
        response=session.get(url=url)
        isNeed=response.json()['isNeed']
        if isNeed:
            print('有验证码：',end="")
            return get_captcha()
        else:
            return False
    def login(execution,password,username,captcha=""):
        jsessionid = requests.utils.dict_from_cookiejar(session.cookies)['JSESSIONID']
        url='http://authserver.nuist.edu.cn/authserver/login;jsessionid={}?service=http://my.nuist.edu.cn/?goto=http://bkxk.nuist.edu.cn/Default_JZ.aspx'.format(jsessionid)
        payload = {"_eventId":"submit",
                    "captcha":captcha,
                    "cllt":"userNameLogin",
                    "execution":execution,
                    "lt":"",
                    "password":password,
                    "username":username,
                   }
        payload=parse.urlencode(payload)
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://authserver.nuist.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        response = session.request("POST", url, headers=headers, data=payload)

    def get_execution():
        url = "http://authserver.nuist.edu.cn/authserver/login?service=http%3A%2F%2Fmy.nuist.edu.cn%2Findex.portal"
        payload = {}
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        response = session.request("GET", url, headers=headers, data=payload)
        html=response.text
        soup=BeautifulSoup(html,'lxml')
        execution=soup.find(id="execution").get('value')
        key=soup.find(id='pwdEncryptSalt').get('value')
        return execution,key
    def aes_cbc(password,key):
        key = key.replace('(^\s+)|(\s+$)','')
        password=randomString(64)+password
        vi=randomString(16)
        BS = AES.block_size  # 这个等于16
        mode = AES.MODE_CBC
        pad = lambda s: s + (BS-len(s))*"\0"  # 用于补全key
        # 用于补全下面的text，上面两个网址就是用以下形式补全的
        pad_txt = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new((pad(key)).encode('utf-8'), mode, vi.encode('utf-8'))
        encrypted = cipher.encrypt((pad_txt(password)).encode('utf-8'))
        #通过aes加密后，再base64加密
        encrypted = base64.b64encode(encrypted)
        return bytes.decode(encrypted)
    def randomString(len):
        data=""
        for i in range(len):
            data=data+random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678')
        return data
    session=requests.session()
    execution,key=get_execution()
    password=aes_cbc(password=password,key=key)
    captcha=checkNeedCaptcha(username=username)
    if captcha!=False:
        login(execution=execution,password=password,username=username,captcha=captcha)
    else:
        login(execution=execution,password=password,username=username)
    if check_result():
        return session.cookies
    else:
        return False
def check_password(student_id, password):
    print('检查学号密码————>')
    print('学号：{}   密码：{}'.format(student_id,password))
    if login(username=student_id,password=password)!=False:
        return True
    else:
        return False