#!/usr/bin/env python3
#coding = utf-8
#author = 阳光流淌007
#date = 2018-03-06
import re
import time
import itchat
from itchat.content import *
from weather import SearchWeather
from package import getPackage
from airlineTicket import getAirline
from trainTicket import searchTrain

TDlist = []
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    replyContent = forselfContent = ""
    fpath = '/Users/zhaoluyang/PythonProject/WeChat_Itchat/downloadFiles/'
    typeDict = {'Picture':'img','Video':'vid','Recording':'fil','Attachment':'fil'}
    typeDict2 = {'Card':'名片','Note':'通知','Sharing':'分享','Map':'位置'}
    replyModel = "收到您于%s发送的【%s】,更多玩法请回复：快递、火车、飞机、天气（回TDD/KTT可退订/开通此功能)" % (time.strftime('%m-%d %H:%M',time.localtime()), msg['Type'])
    if msg['Type'] == 'Text':
        forselfContent = msg['Text']
        try:
            if re.search(r"快乐",msg['Content']) or re.search(r"恭喜",msg['Content']):
                replyContent = "【衷心感谢您的祝福，在此，Lyon祝您：新年快乐！！开开心心😊😊,身体健康[耶][耶]！狗年大吉旺旺旺🐶🐶🐶[發][發][發]】"
                itchat.send('@img@%s' % '/Users/zhaoluyang/PythonProject/WeChat_Itchat/moneyGod.jpg',toUserName=msg['FromUserName'])
            elif re.search(r"天气",msg['Content']) or re.search(r"气温",msg['Content']):
                try:
                    cityname = re.search(r"(天气)(\+)(.*)",msg['Content']).group(3)
                    replyContent = SearchWeather().main(city = cityname)
                except:
                    replyContent ="查询天气请输入：天气+城市名,如：天气+南京"
            elif re.search(r"快递",msg['Content']):
                try:
                    packNum = re.search(r"(快递)(\+)([0-9]+)",msg['Content']).group(3)
                    replyContent = getPackage(package = packNum)
                except:
                    replyContent ="查询快递请输入：快递+运单号，如：快递+12345"
            elif re.search(r"航班",msg['Content']) or re.search(r"飞机",msg['Content']):
                try:
                    info = re.search(r"(航班)(\+)(.*)",msg['Content']).group(3)
                    replyContent = getAirline(string = info)
                except:
                    replyContent ="查询航班请输入：航班+出发地+目的地+时间，如：航班+南京+北京+2018-02-20"
            elif re.search(r"火车",msg['Content']) or re.search(r"余票",msg['Content']):
                try:
                    info2 = re.search(r"(余票)(\+)(.*)",msg['Content']).group(3)
                    replyContent = searchTrain(querystring = info2)
                except:
                    replyContent ="查询火车余票请输入：余票+车型+出发地+目的地+时间，其中可选车型d动车、g高铁、k快速、t特快、z直达（如：余票+dgz+南京+太原+2018-02-25）"
            elif re.search(r"TDD",msg['Content']):
                TDlist.append(msg['FromUserName'])
                itchat.send("😔自动回复功能已关闭，回复KTT可重新开通！",toUserName=msg['FromUserName'])
            elif re.search(r"KTT",msg['Content']):
                if msg['FromUserName'] in TDlist:
                    TDlist.remove(msg['FromUserName'])
                replyContent = "亲🙂，终于等到你~自动回复功能已开通！"
        except Exception as e:
            print(repr(e))

    elif msg['Type'] in typeDict:
        typeSymbol = typeDict.get(msg['Type'],'fil')
        filePath = (fpath + "images/" + msg['FileName']) if typeSymbol=='img' else (fpath + msg['FileName'])
        replyContent = "%s文件: "% msg['Type'] + msg['FileName']
        forselfContent = "%s文件已存储于: "% msg['Type'] + filePath
        try:
            msg.download(filePath)
            print(typeSymbol,filePath)
            asd1 = itchat.send('@%s@%s' % (typeSymbol,filePath),toUserName='filehelper')
            if asd1:
                print('OK,success1!')
            else:
                print(asd1)
                print('Failed!')
                asd2 =  itchat.send_file(filePath,toUserName='filehelper')
                print(asd2)
        except Exception as e:
            print(repr(e))

    elif msg['Type'] in typeDict2:
        if msg['Type'] == 'Map':
            x, y, location = re.search(r"<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,2,3)
            replyContent = forselfContent = ("位置：" + location + "纬度：" + x + " 经度：" + y) if location else (r"位置: " + location)
        else:
            replyContent = forselfContent = typeDict2.get(msg['Type'],'未知类型') + msg['Content']
    else:
        replyContent = forselfContent = "消息"
    itchat.send("【%s】\n%s（昵称：%s）发来%s:【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),friend['NickName'], friend['RemarkName'], msg['Type'], forselfContent),toUserName='filehelper')
    if msg['FromUserName'] in TDlist:
        pass
    else:
        itchat.send(replyModel,toUserName=msg['FromUserName']) if replyContent=='' else itchat.send(replyContent,toUserName=msg['FromUserName'])
    print(msg)
    print("于【%s】收到好友【%s（昵称：%s）】发来【%s】: 【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), friend['NickName'], friend['RemarkName'], msg['Type'], forselfContent))
    print("于【%s】回复：收到您于xxx发送的【%s】,更多玩法。。。%s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), msg['Type'],replyContent)+'\n')
itchat.auto_login(hotReload=True)
itchat.run()
