# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import *

from cdep.helpers import *

class LinkLoader(ItemLoader):
    default_output_processor = TakeFirst()
    title_in = MapCompose(TextHelper.rws, RomanianHelper.beautify_romanian)
