# Installed the version 3.6.1 
# https://github.com/mongodb/mongo-python-driver/tree/3.6.1
import pymongo

class DB(object):

    db_info = {
        'user': None,
        'password': None,
        'host': 'localhost',
        'port': 27017,
        'db_name': 'smm',
        'collection_name': 'smm'
    }

    client  = None
    db = None

    def __init__(self):
        self.client  = pymongo.MongoClient( self.db_info['host'], self.db_info['port'] )
        self.db = self.client.dev
        self.db.name()

    def __getitem__(self, item):
        return getattr(self, item)

    def save(self, data): 
        # smm is the name of collection defined in mongodb
        if self.db.smm.insert_one(data):
            return True
        return False