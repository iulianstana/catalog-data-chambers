# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import *

class StatusLoader(ItemLoader):
    default_output_processor = TakeFirst()
