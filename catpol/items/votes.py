import scrapy


class VotesItem(scrapy.Item):
    vote_id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    person = scrapy.Field()
    person_url = scrapy.Field()
    party = scrapy.Field()
    vote = scrapy.Field()
