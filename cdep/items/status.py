# -*- coding: utf-8 -*-

import scrapy

class StatusItem(scrapy.Item):
    camera_deputatilor = scrapy.Field()
    senat = scrapy.Field()
    status = scrapy.Field()
