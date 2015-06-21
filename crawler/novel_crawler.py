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

import utils
from crawler import CrawlerService

from backend.server import NovelServer, BookServer
from db import mongo


class NovelCrawler:
    def __init__(self):
        self.crawler = CrawlerService()
        #service
        db = mongo.MongoDB(config=mongo.conf)
        self.novel_server = NovelServer(db)
        self.book_server = BookServer(db)

    def crawl(self, input):
        for url in imap(string.strip, input):
            novel = self.crawler.crawl(url)
            #save novel
            self.novel_server.save(novel)

            #convert novel to book
            book = utils.novel_to_book(novel)
            #save book
            self.book_server.add_or_update(book)



