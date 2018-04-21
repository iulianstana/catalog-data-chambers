from scrapy.loader import ItemLoader
import scrapy.loader.processors as processors

import catpol.helpers as helpers


class PersonalDataLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
    name_in = processors.MapCompose(helpers.rws, helpers.beautify_romanian)
    activity_in = processors.Identity()
    formations_in = processors.Identity()
