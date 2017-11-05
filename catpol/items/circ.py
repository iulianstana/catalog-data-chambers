import scrapy


class CircItem(scrapy.Item):
    people = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    leg = scrapy.Field()
    def __init__(self):
        super().__init__()
        self['people'] = []
