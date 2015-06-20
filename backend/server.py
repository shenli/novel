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
        Server.__init__(db)

    def get_novel(self, bid):
        self.db.novel.find_one({'id': bid})

    def add_or_update(self, novel):
        nid = novel['nid']
        #update novel
        self.db.save_novel(nid, novel)


def BookServer(Server):
    def __init__(self, db):
        Server.__init__(db)

    def get_book(self, bid):
        self.db.get_novel(bid)

    def add_or_update(self, book):
        bid = book['bid']
        #if not exist
        if not self.db.exist_book(bid):
            #add
            #format book data, set src
            self.db.save(book)
        else:
            #update
            #get book data
            book = self.get_book(bid)
            if book['src_manual'] == 1:
                pass
            else:
                #select better src
                srcs = book['srcs']
                for src in srcs:
                    pass




