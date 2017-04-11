import unittest
import pickle
import scrapy
import catpol.spiders
import os
import catpol.test.responses

def equal_dict(d1, d2):
    set_keys_d1 = set(d1.keys())
    set_keys_d2 = set(d2.keys())
    if len(set_keys_d1.intersection(set_keys_d2)) != len(set_keys_d1.union(set_keys_d2)):
        return False
    res = True
    for k in d1.keys():
        if k not in d2:
            res = False
            break
        else:
            if type(d1[k]) is dict:
                res = res and equal_dict(d1[k], d2[k])
                if not res:
                    break
            else:
                if d1[k] != d2[k]:
                    res = False
                    break
    return res

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
        is_good = True
        for item in method(self.response):
            was = False
            for result in self.results:
                continue
                was = was or (result == item)
                if was:
                    break
            if not was:
                is_good = False
                break
        self.assertTrue(is_good)
