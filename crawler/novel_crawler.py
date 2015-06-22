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
from crawler_service import CrawlerService

from backend.server import BookServer
from backend.server import NovelServer
from db import mongo


class NovelCrawler:
    def __init__(self):
        self.crawler = CrawlerService()
        #service
        db = mongo.MongoDB(config=mongo.conf)
        self.book_server = BookServer(db)
        self.novel_server = NovelServer(db)

    def crawl(self, input):
        for url in imap(string.strip, input):
            novel = self.crawler.crawl(url)
            #save novel
            succ = self.novel_server.add_or_update(novel)
            if not succ:
                logger.info("save novel %s failed" % novel['nid'])
                return False
            else:
                logger.info("save novel %s success" % novel['nid'])
            #convert novel to book
            logger.debug("Update Book tables")
            #save book
            succ = self.book_server.add_or_update(novel)
            if not succ:
                logger.info("save book %s failed" % novel['bid'])
                return False
            else:
                logger.info("save book %s success" % novel['bid'])
        return True

if __name__ == "__main__":
    cs = NovelCrawler()
    novel = cs.crawl(["http://00xs.com/book/xs11811.php"])
    print json.dumps(novel, indent=2)