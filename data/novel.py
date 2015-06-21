__author__ = 'mac'

import json

"""
category": "\u6b66\u4fa0\u4fee\u771f",
    "status": "\u5df2\u5b8c\u6210",
    "name": "\u9ed1\u8272\u4ea4\u6613\uff0c\u603b\u88c1\u53ea\u5a5a\u4e0d\u7231",
    "author": "\u79be\u7ef4",
    "url": "http://00xs.com/book/xs11811.php",
    "image": "http://00xs.com/files/article/image/11/11811/11811s.jpg",
    "site": "00xs.com",
    "rank": {
      "review_count": 8712
    },
    "chapter_list": [
"""
class Novel:
    def __init__(self):
        self.name = None
