import pymongo
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem

class MongoDBPipeline(object):
    def __init__(self):
        logger = logging.getLogger(__name__)
        self.collection = None
        if 'MONGODB_URI' in settings:
            conn = pymongo.MongoClient(settings['MONGODB_URI'])
            db = conn.get_default_database()
            self.collection = db[settings['MONGODB_COLLECTION']]
            self.obj_id = self.collection.insert({'documents': []})

    def process_item(self, item, spider):
        if self.collection:
            self.collection.update(
                {'_id': self.obj_id},
                {'$push': {'documents': dict(item)}})
            logger = logging.getLogger(__name__)
            logger.debug('Added item to mongo database')
        return item
        
