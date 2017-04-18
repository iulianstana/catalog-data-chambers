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
            if settings['MONGODB_COLLECTION']:
                self.collection = db[settings['MONGODB_COLLECTION']]
                self.obj_id = self.collection.insert({'documents': []})
            else:
                logger.warning('MongoDB URI is set, but collection is not')

    def process_item(self, item, spider):
        if self.collection:
            d = dict(item)
            d['spider'] = spider.name
            self.collection.update(
                {'_id': self.obj_id},
                {'$push': {spider.name: d}})
            logger = logging.getLogger(__name__)
            logger.debug('Added item to mongo database')
        return item
        
