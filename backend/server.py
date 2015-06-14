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


class Server:
    def __init__(self, db):
        self.db = db


class NovelServer(Server):
    def __init__(self, db):
        super.__init__(db)

    def get_novel(self, bid):
        self.db.novel.find_one({'id': bid})

    def add_or_update(self, novel):
        pass


def BookServer(Server):
    def __init__(self, db):
        super.__init__(db)

    def get_novel(self, bid):
        self.db.novel.find_one({'id': bid})

    def add_or_update(self, book):
        pass

