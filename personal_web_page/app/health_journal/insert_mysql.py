# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：personal_web_page -> insert_mysql
@IDE    ：PyCharm
@Author ：Hermes
@Date   ：2020/8/15 20:24
@Desc   ：
=================================================='''
from pymysql import *
class mysql():
    def connect_mysql(self,host='39.99.153.144',port=3306,user='hermes',password='720521',database='hermes',charset='utf8'):
        return connect(host=host,port=port,database=database,user=user,charset=charset,password=password)
    def insert_data(self,student_id,password,email='1993702790@qq.com'):
        if email=="":
            email='1993702790@qq.com'
        try:
            conn = self.connect_mysql()
            cursor = conn.cursor(cursors.DictCursor)
            cursor.execute('''
            REPLACE INTO health_journal (student_id,password,email)
                VALUES ('{}','{}','{}')
            '''.format(student_id,password,email))
            conn.commit()
            return True
        except Exception as e:
            print('插入数据失败,错误信息为：'+str(e))
            print('插入的数据为：')
            print(student_id)
            print(password)
            print(email)
            return False
        finally:
            cursor.close()
            conn.close()
    def remove_account(self,student_id,password):
        try:
            conn = self.connect_mysql()
            cursor = conn.cursor(cursors.DictCursor)
            cursor.execute('''
                   SELECT password FROM health_journal where student_id={}
                   '''.format(student_id))
            result=cursor.fetchall()[0]['password']
            if result==password:
                print('学号：{}密码正确，删除数据'.format(student_id))
                cursor.execute('DELETE FROM health_journal WHERE student_id={}'.format(student_id))
                conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    print('数据库类作为主函数运行')
    mysql().remove_account('2071334047','wang720521')

