from scrapy.loader import ItemLoader
import scrapy.loader.processors as processors

import catpol.helpers as helpers


class ActivityLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
    name_in = processors.MapCompose(helpers.rws, helpers.beautify_romanian)
    dictionary_in = processors.Identity()
