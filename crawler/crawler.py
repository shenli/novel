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
        #html = utils.gbk_to_utf8(html)
        novel = self.parser.parse_novel_page(url, html)
        list_url = novel['list_url']

        html = utils.http_get(list_url, encode='gbk')
        html = self.parser.to_utf8(html)
        chapter_list = self.parser.parse_list_page(list_url, html)
        novel['chapter_list'] = chapter_list
        return novel, chapter_list

    def crawl_content(self, url):
        html = utils.http_get(url, encode='gbk')
        html = self.parser.to_utf8(html)
        content = self.parser.parse_content_page(url, html)
        return content


if __name__ == "__main__":
    import os
    logging.config.fileConfig(os.path.join(os.getcwd(), './conf/logging.conf'))
    logger = logging.getLogger('root')

    crawler = LLXSCrawler()
    novel = crawler.crawl("http://00xs.com/book/xs11811.php")
    print json.dumps(novel, indent=2)