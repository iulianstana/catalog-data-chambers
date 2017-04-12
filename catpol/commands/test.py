import unittest
import catpol.test as tests
from scrapy.commands import ScrapyCommand
import catpol.test.responses

class TestCommand(ScrapyCommand):
    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def long_desc(self):
        return 'Test spiders, loaders, and middlewares'

    def short_desc(self):
        return 'Testing the project'

    def run(self, args, opts):
        suite = unittest.TestSuite()
        for r in catpol.test.responses.FrozenResponses.frozen_responses():
            suite.addTest(tests.TestSpiderParser(
                r['spider'],
                r['method'],
                r['response'],
                r['results']
            ))
        unittest.TextTestRunner().run(suite)
