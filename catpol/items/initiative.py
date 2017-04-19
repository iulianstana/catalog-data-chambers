import scrapy


class InitiativeItem(scrapy.Item):
    title = scrapy.Field()
    status = scrapy.Field()
    author = scrapy.Field()
