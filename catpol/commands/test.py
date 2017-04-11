# -*- coding: utf-8 -*-

import unittest
from scrapy.commands import ScrapyCommand

class Command(ScrapyCommand):
    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def long_desc(self):
        return 'Test spiders, loaders, and middlewares'

    def short_desc(self):
        return 'Testing the project'

    def run(self, args, opts):
        unittest.main()
