# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：xianyu_work -> give_soy_sauce
@IDE    ：PyCharm
@Author ：Hermes
@Date   ：2020/8/30 13:33
@Desc   ：
=================================================='''
import time,requests,threading
userid_set=set()
session=requests.session()
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Unity-Version': '2018.4.21f1',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; VOG-AL00 Build/N2G48H)',
    'Host': 'api.cisgames.cn',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Length': '0',
    'Authorization':'Y2hmYTptOHV0OGlodTRnejo1MDoxMDo1MDpmYWxzZTo6MTU5ODcwMzk4NA=='
}
class giv(threading.Thread):
    receiver=''
    def read_data(self):
        with open('/opt/code_files/personal_web_page/app/darkness_k/userid_set.txt', 'r') as f:
            for line in f:
                line=line.replace('\n','')
                if len(line)!=0:userid_set.add(line)
    def login(self,userid,count=1):
        url = "https://api.cisgames.cn/service/friend/api/friend/login"
        payload = "{\r\n    \"userId\": \"%s\",\r\n    \"appId\": \"025c2961167a457bb62c68448fbe45a0\",\r\n    \"appSecret\": \"4941bc8416a24678b36c31539b54d36d\",\r\n    \"region\": \"\"\r\n}" %(userid)
        response = session.request("POST", url, headers=headers, data=payload)
        try:
            data=response.json()
            token=data['token']
            headers['Authorization']=token
        except Exception as e:
            print('登录失败')
            if count<=5:
                print('多次登录失败')
                self.login(userid,count=count+1)
    def send_coin(self,userid):
        url='https://api.cisgames.cn/service/friend/api/friend/mail/send'
        payload = "{\r\n  \"receiver\": \"%s\",\r\n  \"message\": \"SendCoin-赠送酱油-%s\",\r\n  \"mailType\": 0\r\n}" %(userid,str(int(time.time())))
        payload=payload.encode('utf-8')
        response = session.request("POST", url, headers=headers, data=payload)
        time.sleep(1)
    def send_group_coin(self,receiver):
        for num in range(50):
            userid = userid_set.pop()
            self.login(userid)
            self.send_coin(receiver)
    def run(self):
        if len(self.receiver)>=10:
            self.read_data()
            for count in range(10):
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print(self.receiver,'第%s组' %(count))
                self.send_group_coin(self.receiver)
                time.sleep(9)

if __name__ == '__main__':
    give_soy_sauce=giv()
    give_soy_sauce.receiver='asdqweasf'
    give_soy_sauce.start()