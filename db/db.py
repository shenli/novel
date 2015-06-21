__author__ = 'mac'


class DB:
    def __init__(self):
        self.novel = None
        self.book = None
        self.chapter = None

    #book opts
    def get_book(self, bid):
        pass

    def add_book(self, book):
        pass

    def save_book(self, book):
        pass

    def book_exists(self, bid):
        pass

    #novel opts
    def get_novel(self, nid):
        pass

    def add_novel(self):
        pass

    def update_novel(self, novel):
        pass

    def save_novel(self, novel):
        pass

    def novel_exists(self):
        pass

    #chapter opts
    def get_chapter(self):
        pass

    def save_chapter(self):
        pass