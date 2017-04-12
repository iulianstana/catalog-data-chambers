from scrapy.loader import ItemLoader
import scrapy.loader.processors as processors

import catpol.helpers as helpers

class StatusLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
    status_in = processors.MapCompose(helpers.rws, helpers.beautify_romanian)
