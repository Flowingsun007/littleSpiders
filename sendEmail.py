#!/usr/bin/python3
#_*_ coding:utf-8 _*_
#__author__='Flowingsun'
#__date__='2018.1.22'
"""
用Python的smtplib和email来简单的发送带有附件的邮件，演示是用QQ邮箱发送，发送之前，请手动开启QQ邮箱的smtp服务器并取得授权码passWord。
具体可见知乎文章：https://zhuanlan.zhihu.com/p/33192111
使用方法：
设置好邮发送人邮箱，密码，收件人的邮箱（可以添加多个收件人）；
准备好要插入的附件（这里是图片）包括附件的路径filePath和发送过去要显示的文件名称fileName。
如：
self.sender = 'xxx@qq.com'
self.passWord = 'xxx'
self.string = 'xxx@qq.com;xxx@163.com;xxxxx@163.com'
self.filePath = '/Users/lucifer/Desktop/1.jpg'
self.fileName = 'hello.jpg'
"""
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class sendEmail():
    def __init__(self):
        self.sender = 'xxx@qq.com'#sender是邮件发送人，passWord是服务器授权码，mail_host是服务器地址（这里是QQsmtp服务器）
        self.passWord = 'xxx'
        self.mail_host = 'smtp.qq.com'
        self.string = 'xxx@qq.com;xxx@163.com;xxxxx@163.com'
        self.receivers = []#receivers是邮件接收人，用列表保存，可以添加多个
        self.receivers = self.string.split(';') if ';' in self.string else self.receivers.append(self.string)
        #设置email信息
        self.msg = MIMEMultipart()
        #邮件主题
        self.msg['Subject'] = input('请输入邮件主题：')
        #发送方信息
        self.msg['From'] = self.sender
        #邮件正文是MIMEText:
        self.msg_content = input('请输入邮件内容：')
        self.msg.attach(MIMEText(self.msg_content, 'plain', 'utf-8'))
        # 添加附件就是加上一个MIMEBase，从本地读取一个文件:
        self.filePath = 'xxx'
        self.fileName = 'xxx.jpg'
        with open(self.filePath, 'rb') as f:
            # 设置附件的MIME和文件名，这里是jpg类型,可以换png或其他类型:
            mime = MIMEBase('jpg','jpg', filename=self.fileName)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=self.fileName)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            self.msg.attach(mime)
    def send_main(self):
        #登录并发送邮件
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)#QQsmtp服务器的端口号为465或587
            s.set_debuglevel(1)
            s.login(self.sender,self.passWord)
            #给receivers列表中的联系人逐个发送邮件
            for item in self.receivers:
                self.msg['To'] = to = item
                s.sendmail(self.sender,to,self.msg.as_string())
                print(item,'Success!')
            s.quit()
            print ("All emails have been sent over!")
        except smtplib.SMTPException as e:
            print ("Falied,%s",e)
send = sendEmail()
send.send_main()
