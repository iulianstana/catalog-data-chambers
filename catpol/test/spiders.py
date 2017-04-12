import unittest
import pickle
import scrapy
import catpol.spiders
import os
import catpol.test.responses

class TestSpiderParser(unittest.TestCase):

    def __init__(self, spider, method, response, results):
        self.spider = spider
        self.method = method
        self.response = response
        self.results = results
        super().__init__('runTest')

    def runTest(self):
        settings = scrapy.settings.Settings({
                'SPIDER_MODULES': [
                    'catpol.spiders'
                ]
            }
        )
        spider_loader = scrapy.spiderloader.SpiderLoader.from_settings(settings)
        spider = spider_loader.load(self.spider)()
        method = getattr(spider, self.method)
        for item in method(self.response):
            self.assertTrue(item in self.results)
