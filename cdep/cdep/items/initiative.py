# -*- coding: utf-8 -*-

import scrapy

class InitiativeItem(scrapy.Item):
    title = scrapy.Field(serializer=str)
    status = scrapy.Field()
    author = scrapy.Field()
