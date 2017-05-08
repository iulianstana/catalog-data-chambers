import pymongo
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem

class MongoDBPipeline(object):
    def __init__(self):
        logger = logging.getLogger(__name__)
        self.collection = None
        self.collection_item_branch = dict()
        self.collection_item_branch_obj_id = dict()
        if 'MONGODB_URI' in settings:
            conn = pymongo.MongoClient(settings['MONGODB_URI'])
            db = conn.get_default_database()
            if 'MONGODB_COLLECTION' in settings:
                self.collection = db[settings['MONGODB_COLLECTION']]
                self.obj_id = self.collection.insert({'documents': []})
            if 'MONGODB_COLLECTION_ITEM_BRANCH' in settings:
                for (item_type, collection) in settings['MONGODB_COLLECTION_ITEM_BRANCH'].items():
                    self.collection_item_branch[item_type] = db[collection]
                    self.collection_item_branch_obj_id[item_type] = self.collection_item_branch[item_type].insert({'documents': []})

    def process_item(self, item, spider):
        d = dict(item)
        d['spider'] = spider.name
        item_type = item.__class__.__name__
        if item_type[-4:] == 'Item':
            item_type = item_type[:-4]
        item_type = item_type.lower()
        collection = None
        obj_id = 0
        if item_type in self.collection_item_branch:
            collection = self.collection_item_branch[item_type]
            obj_id = self.collection_item_branch_obj_id[item_type]
        elif self.collection:
            collection = self.collection
            obj_id = self.obj_id
            d['type'] = item_type
        if collection:
            collection.update(
                {'_id': obj_id},
                {'$push': {'documents': d}})
            logger = logging.getLogger(__name__)
            logger.debug('Added \'{}\' item to mongo database'.format(item_type))
        return item
