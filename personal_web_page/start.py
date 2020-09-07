import os,threading
from flask import Flask,render_template,request,send_from_directory
from app.health_journal.check_password import check_password
from app.health_journal.insert_mysql import mysql
from app.darkness_k.give_soy_sauce import giv
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home_page.html')

@app.route('/health_journal/',methods=['GET'])
def health_journal_index():
    return render_template('./health_journal/index.html')

@app.route('/health_journal/check',methods=['POST'])
def submitted_successful():
    student_id=request.form.get('student_id')
    password=request.form.get('password')
    email=request.form.get('email')
    result=check_password(student_id=student_id,password=password)
    if result==True:
        if mysql().insert_data(student_id=student_id,password=password,email=email)==True:
            return render_template('./health_journal/message_template.html',message='提交成功，已将您信息存储至数据库。如需移除用户信息请访问：http://meetrainbow.online/health_journal/remove_account')
        else:
            return render_template('./health_journal/message_template.html',message='用户信息保存至数据库失败，请联系我：<a href="http://wpa.qq.com/msgrd?v=3&uin=1993702790&site=qq&menu=yes">1993702790</a>')
    elif result==False:
        return render_template('./health_journal/message_template.html',message="提交失败，请检查学号及密码后再次提交")
@app.route('/health_journal/remove_account')
def remove_account_page():
    return render_template('./health_journal/remove_account.html')
@app.route('/health_journal/check_remove_account',methods=['POST'])
def remove_account():
    try:
        student_id=request.form.get('student_id')
        password=request.form.get('password')
        result=mysql().remove_account(student_id=student_id,password=password)
        if result==True:
            return render_template('./health_journal/message_template.html', message='用户信息移除成功。')
        else:
            return render_template('./health_journal/message_template.html', message='用户信息错误，请检查学号及密码是否与之前提交的信息一致')
    except:
        return render_template('./health_journal/message_template.html', message='发生未知错误，请联系我QQ：1993702790')

@app.route('/darkness_k/',methods=['GET'])
def darkness_k():
    return render_template('./darkness_k/darkness_k.html')

@app.route('/darkness_k/start',methods=['POST'])
def darkness_k_start():
    archive=request.form.get('archive')
    give_soy_sauce=giv()
    give_soy_sauce.receiver=archive
    give_soy_sauce.start()
    print(archive,'提交成功')
    return render_template('./health_journal/message_template.html', message='提交成功')

@app.route('/time_stamp/time_stamp',methods=['GET','POST'])
def save_time_stamp():
    if request.method=='POST':
        time_stamp=request.form.get('time_stamp')
        with open('./templates/time_stamp/time_stamp.txt','w') as f:
            f.write(time_stamp)
        return time_stamp
    else:
        return render_template('./time_stamp/time_stamp.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)
