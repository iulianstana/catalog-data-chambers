import scrapy


class CountyItem(scrapy.Item):
    people = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
