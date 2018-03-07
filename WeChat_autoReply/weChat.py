#!/usr/bin/env python3
#coding = utf-8
#author = 阳光流淌007
#date = 2018-03-06
"""
程序功能演示和细节见知乎文章：https://zhuanlan.zhihu.com/p/34304821
【程序功能说明】
1.程序主要利用itchat库实现了微信聊天自动回复功能，添加了weather、package、airlineTicket、trainTicket这几个.py文件
将查天气、快递、机票、火车票的功能集成到了微信中，做到了发送关键词如：快递/火车/飞机/天气，自动回复相应内容并返回查询结果的功能！

2.支持的微信消息类型：TEXT文本, PICTURE图片, MAP地点, CARD名片, NOTE通知, SHARING分享, RECORDING语音, ATTACHMENT附件, VIDEO视频
其中查天气、快递、机票、火车票是在TEXT类型的消息中定义的；
MAP即地图类型的消息，自动回复地点名称，经纬度信息；
CARD即名片类型，无特别处理，直接返回msg['content']；
SHARING即分享类型，自动回复分享的链接；
NOTE即通知类型，如果是红包，则回复“谢谢红包打赏💰💰😘😘...”否则msg['content']；
PICTURE、RECORDING、ATTACHMENT、VIDEO支持自动下载到电脑，同时转发给“文件传输助手”查看。

3.支持好友自行退订/开通自动回复（回复TDD退订/KTT开通）退订好友信息保存在——好友退订列表.txt文件中。
【原理】：程序每次运行时自动读取.txt中的文件，将已经退订自动回复的好友信息加载到TDlist中，
做到对于在TDlist中的好友，不调用itchat.send()方法进行自动回复，起到了消息免打扰的功能！
回复TDD，则好友动态加入TDlist列表，并将好友写入.txt中的文件中；
回复KTT，则好友从TDlist移除，更新后的TDlist重新写入到.txt中保存。

4.自动回复好友消息的同时，也会将消息发送给自己的“文件传输助手”做备份！同时通过如下print语句，将消息打印在电脑控制台，方便查看
print("于【%s】收到好友【%s（昵称：%s）】发来【%s】: 【%s】" .......
print("于【%s】回复：收到您于xxx发送的【%s】,更多玩法。。。%s".......

【配置和运行】
本人运行环境：python3.6，macos系统
使用之前请先配置所需的path路径，包括本程序中fpath；
weather.py中pymysql的配置（详见知乎专栏文章：https://zhuanlan.zhihu.com/p/34207133）
"""
import re
import time
import itchat
from itchat.content import *
from weather import SearchWeather
from package import getPackage
from airlineTicket import getAirline
from trainTicket import searchTrain
fpath = '/Users/xxx/WeChat_autoReply/downloadFiles/'
TDlist = []
with open(fpath+u'好友退订列表.txt','r') as f:
    for item in f.readlines():
        TDlist.append(item.strip())

@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    global TDlist
    friend = itchat.search_friends(userName=msg['FromUserName'])
    replyContent = forselfContent = ""
    fpath = '/Users/xxx/WeChat_autoReply/downloadFiles/'
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
                with open(fpath+u'好友退订列表.txt','a+') as f:
                    f.write(msg['FromUserName']+'\n')
                itchat.send("😔自动回复功能已关闭，回复KTT可重新开通！",toUserName=msg['FromUserName'])
            elif re.search(r"KTT",msg['Content']):
                if msg['FromUserName'] in TDlist:
                    TDlist.remove(msg['FromUserName'])
                    with open(fpath+u'好友退订列表.txt','w') as f:
                        f.write('\n'.join(TDlist))
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
        elif msg['Type'] == 'Sharing':
            replyContent = forselfContent = typeDict2.get(msg['Type'],'未知类型') + "链接：\n" + msg['Url']
        elif msg['Type'] == 'Note':
            if "红包" in msg['Content']:
                replyContent = forselfContent = ("(｡◕‿‿◕｡)谢谢红包打赏💰💰😘😘") if "红包" in msg['Content'] else (typeDict2.get(msg['Type'],'未知类型') + msg['Content'])
        elif msg['Type'] == 'Card':
            replyContent = forselfContent = typeDict2.get(msg['Type'],'未知类型消息') + msg['Content']
    else:
        replyContent = forselfContent = "未知类型消息"
    itchat.send("【%s】\n%s（昵称：%s）发来%s:【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),friend['NickName'], friend['RemarkName'], msg['Type'], forselfContent),toUserName='filehelper')
    if msg['FromUserName'] in TDlist:
        pass
    else:
        itchat.send(replyModel,toUserName=msg['FromUserName']) if replyContent=='' else itchat.send(replyContent,toUserName=msg['FromUserName'])
    #查看详细信息可以用print(msg)
    print("于【%s】收到好友【%s（昵称：%s）】发来【%s】: 【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), friend['NickName'], friend['RemarkName'], msg['Type'], forselfContent))
    print("于【%s】回复：收到您于xxx发送的【%s】,更多玩法。。。%s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), msg['Type'],replyContent)+'\n')
itchat.auto_login(hotReload=True)
itchat.run()
