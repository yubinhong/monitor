#!/usr/bin/env python
#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen,Request
from urllib.parse import urlencode


mailto_list = ['xxxxxxxxxxx']
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "xxxxxxx"  # 用户名
mail_pass = "xxxxxxx"  # 口令
mail_postfix = "126.com"  # 发件箱的后缀
url="http://api.110monitor.com/alert/api/event" #外部告警API地址


def send_mail(to_list, sub, content):
    me =  "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def send_api(appkey,content,alertid,hostname):
    data={
        "app": str(appkey),
        "eventId": str(alertid),
        "eventType": "trigger",
        "alarmName": "alarm on machine %s" % (hostname),
        "entityName": "host-%s" % (hostname),
        "entityId": "host-%s" % (hostname),
        "priority": 2,
        "alarmContent": str(content),
    }
    temp_data=urlencode(data)
    req=Request(url=url,data=temp_data.encode(encoding='utf-8',errors='ignore'),method='POST')
    f=urlopen(req,timeout=120)
    return f.read()

if __name__ == '__main__':
    if send_mail(mailto_list, "hello", "hello world！"):
        print("发送成功")
    else:
        print("发送失败")
