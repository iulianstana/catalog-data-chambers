import pymongo
import logging
import datetime

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class MongoDBPipeline(object):
    def __init__(self):
        logger = logging.getLogger(__name__)
        client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        logger.debug(
            'Connected to MongoDB {}:{}'.format(
                settings['MONGODB_SERVER'],
                settings['MONGODB_PORT']))
        db = client[settings['MONGODB_DB']]
        logger.debug(
            'Accessed database {}'.format(
                settings['MONGODB_DB']))
        db.authenticate(
            settings['MONGODB_USER'], 
            settings['MONGODB_PASS'],
            mechanism = settings['MONGODB_MECH'],
            source = settings['MONGODB_SOURCE'])
        logger.debug('Authenticated!')
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.obj_id = self.collection.insert({'documents': []})
        logger.debug(
            'Accessed collection {} in database {}'.format(
                settings['MONGODB_COLLECTION'],
                settings['MONGODB_DB']))

    def process_item(self, item, spider):
        self.collection.update(
            {'_id': self.obj_id},
            {'$push': {'documents': dict(item)}})
        logger = logging.getLogger(__name__)
        logger.debug('Added item to mongo database')
        return item
        
