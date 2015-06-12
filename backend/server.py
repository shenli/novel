__author__ = 'shenli'


import sys
sys.path.append("../")
import json


"""
Novel:
    bid: bookid
    md5: name + auth + salt
    name:
    author:
    srcs: did list
    curr_src: bests src
    manual: assign curr_src manually or auto
    insert_time:
    update_time:

Book:
    did: bookid + siteid
    name/auth/desc/chapter_len/update_time/insert_time/site/url/cover_image
    chapters { title, url, update_time, cid}

Chapter:
    cid
    title/url/content



"""


class NovelServer:
    def __init__(self, db):
        self.db = db

    def get_novel(self, bid):
        self.db.novel.find_one({'id': bid})