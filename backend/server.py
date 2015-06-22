__author__ = 'shenli'


import sys
sys.path.append("../")
import time

from crawler.utils import novel_to_book


"""
Novel:
    bid: bookid
    md5: name + auth + salt
    name:
    author:
    srcs: [{src: site, did, clen, score},]
    curr_src: bests src
    manual_src: assign curr_src manually or auto
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
        Server.__init__(self, db)

    def get(self, bid):
        return self.db.get_novel({'id': bid})

    def add_or_update(self, novel):
        if 'nid' not in novel:
            return False
        nid = novel['nid']
        dbnovel = self.db.get_novel(nid)
        if dbnovel is None:
            return self.db.save_novel(novel)
        else:
            return self.db.update_novel(novel)
        #update_time


class BookServer(Server):
    def __init__(self, db):
        Server.__init__(self, db)

    def get_book(self, bid):
        return  self.db.get_book(bid)

    def add_or_update(self, novel):
        if 'bid' not in novel:
            return False
        bid = novel['bid']
        dbbook = self.db.get_book(bid)
        #if not exist
        if not self.db.book_exists(bid):
            #add new book
            book = novel_to_book(novel)
            return self.db.save_book(book)

        #update book info
        #get book data

        #select better src
        srcs = dbbook['srcs']
        curr_src = dbbook.get('curr_src')
        #update len = 0
        change = True
        nid = novel['nid']
        curr_len = 0
        save_data = {}
        for src in srcs:
            if src["id"] == nid:
                if src["clen"] == novel['chapters']:
                    change = False
                    break
                change = True
                src["clen"] = novel['chapters']
                save_data['srcs'] = srcs
            if src["id"] == curr_src:
                curr_len = src["clen"]

        if curr_len < novel["chapters"] and dbbook.get('manual_src', 0) == 0:
            save_data['curr_src'] = nid

        if len(save_data) > 0:
            save_data['bid'] = bid
            save_data["update_time"] = time.time()
            #query = {"bid": bid}
            return self.db.update_book(save_data)
        return True