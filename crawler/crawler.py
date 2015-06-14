__author__ = 'mac'


import sys
import json
import requests
import logging
import logging.config

from parser import LLXSParser
import utils

class Crawler:
    def __init__(self):
        pass

    def crawl(self, url):
        pass


class LLXSCrawler(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.parser = LLXSParser()

    def crawl(self, url):
        #get novel page
        html = utils.http_get(url, encode="gbk")
        html = self.parser.to_utf8(html)
        novel = self.parser.parse_novel_page(url, html)

        print json.dumps(novel, indent=2, separators=(',', ': '))

if __name__ == "__main__":
    import os
    logging.config.fileConfig(os.path.join(os.getcwd(), './conf/logging.conf'))
    logger = logging.getLogger('root')

    crawler = LLXSCrawler()
    crawler.crawl("http://00xs.com/book/xs11811.php")