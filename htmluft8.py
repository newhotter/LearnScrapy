# -*- coding: utf-8 -*-
__author__ = 'Haoa'
import os
import re
b = ''' <head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> </head>'''

web = open("test.html")
s = web.read()
web.close()
a = s.split('\n')
a.insert(3,b)
s = '\n'.join(a)
web = open("test.html",'w')
web.write(s)
web.close()
