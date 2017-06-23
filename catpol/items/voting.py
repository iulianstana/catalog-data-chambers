import scrapy


class VotingItem(scrapy.Item):
    vote_id = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    people_present = scrapy.Field()
    abstention = scrapy.Field()
    vote_yes = scrapy.Field()
    vote_no = scrapy.Field()
    vote_ab = scrapy.Field()
    votes = scrapy.Field()
