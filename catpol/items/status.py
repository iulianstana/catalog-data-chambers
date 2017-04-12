import scrapy

class StatusItem(scrapy.Item):
    cdep = scrapy.Field()
    senat = scrapy.Field()
    status = scrapy.Field()
