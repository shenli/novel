__author__ = 'shenli'

import json
import pymongo
from db import DB


conf = {
    "host": "localhost",
    "port": 27017,
    #"username": "novel",
    #"password": "novelpwd",
    "database": "novel"
}


class MongoDB(DB):

    def __init__(self, config=conf):
        self.client = pymongo.MongoClient(config["host"], config["port"])
        self.db = self.client[config["database"]]
        if 'username' in config and 'password' in config:
            self.db.authenticate(config['username'], config['password'])
        self.book = self.db.book
        self.novel = self.db.novel
        self.chapter = self.db.chapter

        #create_index
        self.book.create_index("bid")
        self.novel.create_index("nid")
        self.chapter.create_index("cid")

    def get_all_books(self):
        books = self.book.find({}, {"_id": False})
        return books

    #book opts
    def get_book(self, bid):
        if bid is None:
            return None
        x = self.book.find_one({"bid": bid}, {"_id": False})
        if x is None:
            return None
        return x

    def add_book(self, book):
        x = self.book.insert_one(book)
        if x is not None:
            return True
        return False

    def save_book(self, book):
        return self.add_book(book)

    def update_book(self, data):
        if 'bid' not in data:
            return False
        query = {'bid': data['bid']}
        del data["bid"]
        doc = {"$set": data}
        return self.book.update(query, doc)

    def book_exists(self, bid):
        x = self.get_book(bid)
        if x is None:
            return False
        return True

    #novel opts
    def get_novel(self, nid):
        if nid is None:
            return None
        x = self.novel.find_one({"nid": nid}, {"_id": False})
        if x is None:
            return None
        return x

    def search_novel(self, query):
        x = self.novel.find(query, {"_id": False})
        return x

    def add_novel(self, novel):
        x = self.novel.insert_one(novel)
        print x
        if x is not None:
            return True
        return False

    def update_novel(self, data):
        if 'nid' not in data:
            return False
        query = {'nid': data['nid']}
        #del data["nid"]
        doc = {"$set": data}
        return self.novel.update(query, doc)

    def save_novel(self, novel):
        return self.add_novel(novel)

    def novel_exists(self, nid):
        x = self.get_novel(nid)
        if x is None:
            return False
        return True

    #chapter opts
    def get_chapter(self):
        pass

    def save_chapter(self):
        pass


def run():
    db = MongoDB(conf)
    for x in db.get_all_books():
        print x['bid'], x

if __name__ == "__main__":
    run()
