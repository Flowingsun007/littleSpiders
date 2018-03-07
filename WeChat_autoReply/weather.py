#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
#__author__='阳光流淌007'
#__date__ = '2018-03-06'
import re
import pymysql
import requests
from bs4 import BeautifulSoup

class SearchWeather():
    def __init__(self):
        self.URL = 'http://www.weather.com.cn/weather/101190101.shtml'
        self.HEADERS ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.CONNECTION = pymysql.connect(host='localhost',user='root',password='XXX',db='XXX',charset='utf8',cursorclass=pymysql.cursors.DictCursor)

    def getcityCode(self,cityName):
        SQL = "SELECT cityCode FROM cityWeather WHERE cityName='%s'" % cityName
        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(SQL)
                self.CONNECTION.commit()
                result = cursor.fetchone()
                cityCode = result['cityCode']
                return cityCode
        except Exception as e:
            print(repr(e))

    def getWeather(self,cityCode,cityname):
        url = 'http://www.weather.com.cn/weather/%s.shtml' % cityCode
        details = "日期|天气|最高温|最低温|风向|风力\n"
        try:
            html = requests.get(url,headers = self.HEADERS)
            html.encoding='utf-8'
            soup=BeautifulSoup(html.text,'lxml')
            for day in soup.find("div", {'id': '7d'}).find('ul').find_all('li'):
                date,detail = day.find('h1').string, day.find_all('p')
                title = detail[0].string
                templow = detail[1].find("i").string
                temphigh = detail[1].find('span').string if detail[1].find('span')  else ''
                wind,direction = detail[2].find('span')['title'], detail[2].find('i').string
                if temphigh=='':
                    details += '你好，【%s】今天白天：【%s】，温度：【%s】，%s：【%s】\n' % (cityname,title,templow,wind,direction)
                else:
                    details += (date + title + "【" + templow +  "~"+temphigh +'】' + wind + direction + "\n")
        except Exception as e:
            print(repr(e))
            details += repr(e)
        finally:
            return details

    def main(self,city='南京'):
        cityCode = self.getcityCode(city)
        detail = self.getWeather(cityCode,city) if cityCode else "亲，您输入的城市名称有误！"
        return detail

if __name__ == "__main__":
    weather = SearchWeather()
    weather.main()
