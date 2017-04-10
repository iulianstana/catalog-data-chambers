# -*- coding: utf-8 -*-

import scrapy

class LinkItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
