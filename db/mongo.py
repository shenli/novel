__author__ = 'shenli'

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

    #book opts
    def get_book(self):
        pass

    def add_book(self):
        pass

    def save_book(self):
        pass

    def book_exists(self):
        pass

    #novel opts
    def get_novel(self, nid):
        if nid is None:
            return None
        x = self.novel.find_one({"nid": nid})
        if x is None:
            return None
        return x

    def add_novel(self, novel):
        self.novel.insert_one(novel)

    def update_novel(self, novel):
        pass

    def save_novel(self, novel):
        x = self.novel.insert_one(novel)
        if x is not None:
            return True
        return False

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
    print db.novel_exists("1")

if __name__ == "__main__":
    run()
