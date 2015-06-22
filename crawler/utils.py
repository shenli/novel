__author__ = 'mac'

import logging
import subprocess
import requests
import urlparse
import hashlib

HEADERS = {
    "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
    "Accept-Charset":"UTF-8,*;q=0.5",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1"
}


logger = logging.getLogger('root')


def http_get(url, headers=HEADERS, try_cnt=3, encode=None):
    tc = 0
    while tc < try_cnt:
        try:
            r = requests.get(url, headers=headers)
            if encode is not None:
                r.encoding = encode
        except Exception, e:
            tc += 1
            logger.error("Exception in http_get", e)
            continue
        html = r.text
        return html
    return None


def to_unicode(content):
    child = subprocess.Popen(["./htmldecode"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return child.communicate(content)[0]

def gbk_to_utf8(str):
    #child = subprocess.Popen(["iconv", "-f", "gbk", "-t", "utf-8"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #return child.communicate(str)[0]
    str = str.decode("gbk").encode("utf-8")
    return str


def try_encode(str):
    try:
        str = str.encode("utf-8")
        return str
    except:
        return str


def to_utf8(content):
    content = to_unicode(content)
    content = try_encode(content)
    return content



def make_book_id(name, author):
    txt = name + "#" + author + "#xiaoshuov.com"
    m = hashlib.md5()
    m.update(txt)
    bid = m.hexdigest()[:16]
    return bid


def make_novel_id(name, author, site):
    txt = name + "#" + author + "#" + site
    m = hashlib.md5()
    m.update(txt)
    nid = m.hexdigest()[:16]
    return nid


def make_chapter_id(url):
    txt = url
    m = hashlib.md5()
    m.update(txt)
    cid = m.hexdigest()[:16]
    return cid


def uniform_hostname(hn):
    return hn


def get_site(url):
    up = urlparse.urlparse(url)
    hostname = up.hostname
    return hostname


def get_url_path(url):
    idx = url.rfind('/')
    return url[:idx + 1]


def novel_to_book(novel):
    book = {}
    cpy_attrs = ["bid", "name", "author", "status", "category", "rank", "image", "chapters", "update_time"]
    for attr in cpy_attrs:
        if attr in novel:
            book[attr] = novel[attr]
    book["srcs"] = [{"id": novel["nid"], "site": novel["site"], "clen": novel["chapters"]}]
    book["src"] = novel["nid"]
    book["curr_src"] = novel["nid"]
    return book
