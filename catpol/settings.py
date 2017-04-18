BOT_NAME = 'catpol'
FEED_EXPORT_ENCODING = 'utf-8'
SPIDER_MODULES = ['catpol.spiders']
NEWSPIDER_MODULE = 'catpol.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'INFO'

COMMANDS_MODULE = 'catpol.commands'

ITEM_PIPELINES = {'catpol.pipelines.MongoDBPipeline': 300}

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017 
MONGODB_DB = 'catalog'
MONGODB_COLLECTION = 'collections'
MONGODB_USER = 'user'
MONGODB_PASS = 'pass'
MONGODB_SOURCE = None
MONGODB_MECH = 'SCRAM-SHA-1'
