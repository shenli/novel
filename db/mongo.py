__author__ = 'shenli'

import pymongo


conf = {
    "host": "localhost",
    "port": 27017,
    "username": "novel",
    "password": "novelpwd",
    "database": "novel"
}


class MongoDB:
    def __init__(self, config=conf):
        self.conn = pymongo.Connection(config["host"], config["port"])
        self.db = self.conn[config["database"]]
        self.db.authenticate(config['username'], config['password'])

    def save(self):
        pass

