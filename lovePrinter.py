#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
#__author__='阳光流淌007'
#__date__='2018.1.22'
"""
实现命令行动态打印一段爱心字符画的效果，打印的话内容可自定义。
如：words = Dear lili, Happy Valentine's Day! Lyon Will Always Love You Till The End! ♥ Forever!  ♥！

P.S：
1.添加item = item + ' '可以实现文字中间空格的效果；改变time.sleep的值，可以调节爱心打印的速度！
2.可以添加emoji表情符和类似颜文字的效果😊❤️，不过由于字符的宽度问题，可能会影响打印出的爱心形状！
"""
import time
words = input('Please input the words you want to say!:')
for item in words.split():
    print('\n'.join([''.join([(item[(x-y) % len(item)] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(12, -12, -1)]))
    time.sleep(1);
