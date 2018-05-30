BOT_NAME = 'catpol'
FEED_EXPORT_ENCODING = 'utf-8'
SPIDER_MODULES = ['catpol.spiders']
NEWSPIDER_MODULE = 'catpol.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'INFO'

COMMANDS_MODULE = 'catpol.commands'

ITEM_PIPELINES = {'catpol.pipelines.MongoDBPipeline': 300}

MONGODB_URI = 'mongodb://localhost:27017/catalog'
MONGODB_COLLECTION = 'raw_parsed_data'
MONGODB_COLLECTION_ITEM_BRANCH = {'item_type': 'collection'}
