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
        novel['site'] = site
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

        novel['bid'] = utils.make_book_id(name, author)
        novel['nid'] = utils.make_novel_id(name, author, site)

        desc = info.find('div', {'class': 'intro'})
        novel['desc'] = desc.text.encode("utf-8").replace("&nbsp;", "").strip().lstrip('\r')

        infos = info.find('tr', {'valign': 'top'})
        if infos is not None:
            tds = infos.findAll('td')
            for td in tds:
                txt = td.text.encode('utf-8')
                tmp = txt.split('：', 1)
                if len(tmp) != 2:
                    continue
                if tmp[0] == '文章分类':
                    novel['category'] = tmp[1]
                elif tmp[0] == '文章状态':
                    novel['status'] = tmp[1]
        options = info.find('div', {'class': 'option'})
        if options is not None:
            list_page = options.find('span' , {'class': 'btopt'}).a.get('href')
            novel['list_url'] = list_page
        return novel

    def parse_list_page(self, list_url, html):
        soup = BeautifulSoup(html)
        if soup is None:
            print "soup is None"
            return None
        book_list = soup.find('div', {'class': 'booklist'})
        if book_list is None:
            return None
        chapters = []
        base_url = utils.get_url_path(list_url)
        for li in book_list.findAll('li'):
            try:
                url = li.span.a.get('href').encode("utf-8")

                title = li.text.encode('utf-8')
                chapter = {'url': base_url + url, "title": title,
                           'cid': utils.make_chapter_id(base_url + url)}
                chapters.append(chapter)
            except:
                pass
        return  chapters

    def parse_content_page(self, url, html):
        soup = BeautifulSoup(html)
        if soup is None:
            print "soup is None"
            return None

        book_list = soup.find('div', {'id': 'content'})
        return book_list.encode("utf-8")

