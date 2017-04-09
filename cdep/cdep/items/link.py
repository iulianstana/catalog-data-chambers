# -*- coding: utf-8 -*-

import scrapy

class LinkItem(scrapy.Item):
    title = scrapy.Field(serializer=str)
    href = scrapy.Field(serializer=str)
