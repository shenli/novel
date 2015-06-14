# -*- coding: utf-8 -*-
__author__ = 'mac'

import utils

from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        pass

    def parse_novel_page(self):
        pass

    def parse_list_page(self):
        pass

    def parse_content_page(self):
        pass

    def to_utf8(self, str):
        str = utils.to_utf8(str)
        return str


class LLXSParser(Parser):
    def __init__(self):
        Parser.__init__(self)

    def to_utf8(self, str):
        str = str.encode("utf-8")
        return str

    def parse_novel_page(self, url, html):
        soup = BeautifulSoup(html)
        if soup is None:
            print "soup is None"
            return None
        novel = {'url': url}
        site = utils.get_site(url)
        box_intro = soup.find('div', {'class': 'box_intro'})
        pic = box_intro.find('div', {'class': 'pic'})
        novel['image'] = pic.img.get('src')

        info = box_intro.find('div', {'class': 'box_info'})
        if info is None:
            return None

        rank = {}
        ren = info.find('em', {'id': 'ren'})
        if ren is not None:
            rank['review_count'] = int(ren.text.encode('utf-8'))
        novel['rank'] = rank

        h1 = info.find('h1')
        if h1 is None:
            return None

        name_author = h1.text.encode('utf-8')
        if "作者：" not in name_author:
            return None
        name, author = name_author.split("作者：")
        novel['name'] = name.strip()
        novel['author'] = author.strip()

        bid = utils.make_book_id(name, author)
        nid = utils.make_novel_id(name, author, site)

        return novel

