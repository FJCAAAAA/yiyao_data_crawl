#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : OCR.py
@Author: Fengjicheng
@Date  : 2020/1/3
@Desc  :
'''

# -*- coding:utf-8 -*-
from PIL import Image
import pytesseract
import time

start = time.clock()  # 开始计时
# ---------主要代码------------
im = Image.open('yao.jpg')
code = pytesseract.image_to_string(im)
print(u'验证码:' + str(code))
# ---------------------------------
end = time.clock()  # 结束计时

print(u'运行时间:' + str(end - start))