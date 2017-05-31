import scrapy


class PleneryTimeItem(scrapy.Item):
    name = scrapy.Field()
    duration = scrapy.Field()
    url = scrapy.Field()
