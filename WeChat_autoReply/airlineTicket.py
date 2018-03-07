#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
#__author__='阳光流淌007'
#__date__ = '2018-03-06'
import re
import json
import requests
def getAirline(string):
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    air_company = {"G5":"华夏航空","9C":"春秋航空","MU":"东方航空","NS":"河北航空","HU":"海南航空","HO":"吉祥航空","CZ":"南方航空","FM":"上海航空","ZH":"深圳航空","MF":"厦门航空","CA":"中国国航","KN":"中国联航"}
    airlines = "航空公司|航班|机场|出发到达时间|机票价格|机场建设费:\n"
    url_station = 'http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?CR_2017_07_18_00_00_00'
    #stations为航空公司代号字典譬如：南京禄口国际机场=ABC...
    stations = dict(re.findall(u'([\u4e00-\u9fa5]+)\(([A-Z]+)\)', requests.get(url_station,verify=False).text))
    infolist = string.split('+')
    arguments = {
    'from':infolist[0],
    'to':infolist[1],
    'date':infolist[2],
    }
    fromCity = stations[arguments['from']]
    toCity = stations[arguments['to']]
    tripDate = arguments['date']
    url = ("http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1={}&ACity1={}&SearchType=S&DDate1={}&IsNearAirportRecommond=0&LogToken=0dc7fd99662349069c123f0a8bfcae95&rk=7.387068566272421154925&CK=51BF6E070FF329F1DDD90CEF097B4B86&r=0.5811166470511521823610").format(fromCity,toCity,tripDate)
    try:
        r = requests.get(url,headers = headers,verify=False)
        for item in r.json()['fis']:
            try:
                strs = air_company[item['alc']]
            except KeyError:
                strs = item['alc']
            datail = "【"+strs+'|'+item['fn']+'|'.join([item['dpbn'],item['apbn']+"|"])+'\n'.join([item['dt']+"|"+item['at']])+'|'+str(item['lp'])+'|'+str(item['tax'])+"】\n"
            airlines += datail
    except Exception as e:
        print(repr(e))
        airlines += repr(e)
    finally:
        return airlines

if __name__ == '__main__':
    getAirline(string = '南京+北京+2018-02-20')
