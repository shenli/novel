# -*- coding: utf-8 -*-
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
from backend.server import OperateServer
from db import mongo

db = mongo.MongoDB(config=mongo.conf)


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.book_server = BookServer(db)
        self.novel_server = NovelServer(db)
        self.operate_server = OperateServer(db)

    def get_para_str(self, pname):
        x = self.get_argument(pname, None)
        if x is not None:
            return x.encode("utf-8")


catgegory = {}

class MainHandler(BaseHandler):

    def get(self):
        bid = self.get_para_str("bid")
        #get hotbooks
        hot_ids = self.operate_server.get_hot_books()
        hot_books = []
        for hid in hot_ids:
            b = self.book_server.get_book(hid)
            if b is not None:
                desc = b.get("desc", "")
                if desc == "":
                    b["desc"] = "热门小说"
                if len(desc) > 75:
                    b['desc'] = desc[:75] + "..."
                hot_books.append(b)
        cats = self.operate_server.get_categories()
        cat_books = {}
        for cat in cats:
            cat_books[cat] = self.novel_server.get_novel_by_category(cat)
        self.render("template/index.html", hot_books=hot_books, cats=cats, cat_books= cat_books)



class BookHandler(BaseHandler):

    def get_title(self, book):
        return "%s_%s_最新章节" % (book.get("name", "").encode("utf-8"), book.get("author", "").encode("utf-8"))

    def get(self):
        bid = self.get_para_str("bid")
        if bid is None:
            self.write("Miss Bid")
        else:
            book = self.book_server.get_book(bid)
            if book is not None:
                curr_src = book.get('curr_src', None)
                book = self.novel_server.get_novel(curr_src)
                desc = book.get("desc", "")
                """
                if len(desc) > 300:
                    desc = desc[:300] + "..."
                    book["desc"] = desc
                """
                self.render("template/book.html", title=self.get_title(book), book=book)
            else:
                self.write("找不到该小说！请重新查找")


class CategoryHandler(BaseHandler):

    def get(self, cat):
        cats = self.operate_server.get_categories()
        books = self.novel_server.get_novel_by_category(cat)
        cbooks = []
        for b in books:
            cbooks.append(b)
        for b in cbooks:
            desc = b.get("desc", "")
            if len(desc) == 0:
                b['desc'] = u"热门小说"
            elif len(desc) > 75:
                b["desc"] = desc[:75]
        self.render("template/cat.html", cat=cat.encode("utf-8"), books=cbooks, cats=cats)



class ComponentHandler(BaseHandler):

    def get(self, component):
        self.render("template/" + component)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "js_path": os.path.join(os.path.dirname(__file__), "js"),
    "css_path": os.path.join(os.path.dirname(__file__), "css"),
    "image_path": os.path.join(os.path.dirname(__file__), "img"),
    "fonts_path": os.path.join(os.path.dirname(__file__), "fonts"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "debug": 1,
    }

application = tornado.web.Application(
    [(r"/", MainHandler),
     (r"/book", BookHandler),
     (r"/cat/(.*)", CategoryHandler),
     (r"/component/(.*.html)", ComponentHandler),
     (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path=settings['js_path'])),
     (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path=settings['css_path'])),
     (r"/img/(.*)", tornado.web.StaticFileHandler, dict(path=settings['image_path'])),
     (r"/fonts/(.*)", tornado.web.StaticFileHandler, dict(path=settings['fonts_path'])),
    ], **settings)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()