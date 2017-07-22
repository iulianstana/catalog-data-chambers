import scrapy


class PersonalDataItem(scrapy.Item):
    name = scrapy.Field()
    birthdate = scrapy.Field()
    activity = scrapy.Field()
    url = scrapy.Field()
    eurogroup = scrapy.Field()
    birthplace = scrapy.Field()
    party = scrapy.Field()
