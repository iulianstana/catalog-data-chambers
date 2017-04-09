# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import *

from cdep.helpers import *

class InitiativeLoader(ItemLoader):
    default_output_processor = TakeFirst()
    title_in = MapCompose(TextHelper.rws, RomanianHelper.beautify_romanian)
    author_in = MapCompose(TextHelper.rws, RomanianHelper.beautify_romanian)
