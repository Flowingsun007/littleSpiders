#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
#__author__='阳光流淌007'
#__date__ = '2018-03-06'
"""
程序利用12306的API，用来查询火车票余票信息，添加了同时显示硬座票价的功能(url3和url4...)。
使用方式：余票+车型+出发地+目的地+时间（其中可选车型d动车、g高铁、k快速、t特快、z直达）
例：余票+dgz+南京+太原+2018-03-25
"""
import re
import json
import requests

def searchTrain(querystring):
    infolist = querystring.split('+')
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
    details = '【车次|车站|发到时间(历时)|商务座|特等座|一等|二等|高级软卧|软卧|硬卧|软座|硬座(票价)|无座|其他】\n'
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
    try:
        requests.packages.urllib3.disable_warnings()
        stations = dict(re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', requests.get(url,verify=False).text))
        arguments = {
        'option':infolist[0],
        'from':infolist[1],
        'to':infolist[2],
        'date':infolist[3]
        }
        fromStation = stations[arguments['from']]
        toStation = stations[arguments['to']]
        tripDate = arguments['date']
        options = ''.join([item for item in arguments['option']])
        url2 = ('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(tripDate,fromStation,toStation)
        requests.packages.urllib3.disable_warnings()#在语句前加上此句即可不会被报错urllib3/connectionpool.py:843: InsecureRequestWarning: Unverified HTTPS request
        available_trains = requests.get(url2,headers = headers,verify=False).json()['data']['result']
        for item in available_trains:
            cm = item.split('|')
            train_no, train_name = cm[2], cm[3]
            initial = train_name[0].lower()
            if not options or initial in options:
                fromstationNo = tostationNo = ""
                url3 = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={}&from_station_telecode={}&to_station_telecode={}&depart_date={}".format(train_no,cm[6],cm[7],tripDate)
                try:
                    requests.packages.urllib3.disable_warnings()
                    for item in requests.get(url3,headers = headers,verify=False).json()['data']['data']:
                        if arguments['from'] in item['station_name']:
                            fromstationNo = item['station_no']
                        if arguments['to'] in item['station_name']:
                            tostationNo = item['station_no']
                    url4 = ('https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types=1413&train_date={}'.format(train_no,fromstationNo,tostationNo,tripDate))
                    requests.packages.urllib3.disable_warnings()
                    tickectPrice = requests.get(url4,headers = headers,verify=False).json()['data']['WZ']
                except Exception as e:
                    details += repr(e)
                    print(repr(e))
                price = tickectPrice if tickectPrice else ""
                train = [
                '【'+train_name,'-'.join([cm[6],cm[7]]),'-'.join([cm[8],cm[9]])+'('+cm[10]+')',cm[32],cm[25],
                cm[31],cm[30],cm[21],cm[23],cm[28],cm[24],cm[29]+'('+price+')',cm[26],cm[22]+'】\n'
                ]
                details += ' | '.join(train)
    except Exception as f:
        details += repr(f)
        print(repr(f))
    finally:
        return details

if __name__ == '__main__':
    searchTrain(querystring = 'dgz+南京+太原+2018-02-25')
