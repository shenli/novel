__author__ = 'mac'

import os
import sys
sys.path.append("../")
import json
import string
from itertools import imap

import logging
import logging.config

logging.config.fileConfig(os.path.join(os.getcwd(), '../conf/logging.conf'))
logger = logging.getLogger('root')


import tornado.ioloop
import tornado.web

from backend.server import BookServer
from backend.server import NovelServer
from db import mongo

db = mongo.MongoDB(config=mongo.conf)


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.book_server = BookServer(db)
        self.novel_server = NovelServer(db)

    def get_para_str(self, pname):
        x = self.get_argument(pname, None)
        if x is not None:
            return x.encode("utf-8")


class MainHandler(BaseHandler):

    def get(self):
        bid = self.get_para_str("bid")
        if bid is None:
            self.write("Miss Bid")
        else:
            book = self.book_server.get_book(bid)
            self.write(json.dumps(book, indent=2))

application = tornado.web.Application([
    (r"/", MainHandler),
    ])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()