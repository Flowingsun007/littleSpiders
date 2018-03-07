#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
#__author__='阳光流淌007'
#__date__ = '2018-03-06'
import itchat
itchat.auto_login()
for friend in itchat.get_friends(update=True)[0:]:
    print(friend['NickName'],friend['RemarkName'],friend['Sex'],friend['Province'],friend['Signature'])
    img = itchat.get_head_img(userName=friend["UserName"])
    path = "/Users/xxx/Wechat_headerImages/HeadImages/"+friend['NickName']+"("+friend['RemarkName']+").jpg"
    with open(path,'wb') as f:
        f.write(img)
itchat.run()
