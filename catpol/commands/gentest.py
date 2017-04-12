import os
import time
import pickle
import logging
import scrapy
import json

import catpol.spiders

from selenium import webdriver
from scrapy.http import Response
from urllib.parse import urlparse
from scrapy.exceptions import UsageError
from catpol.test.responses import FrozenResponses

class GentestCommand(scrapy.commands.ScrapyCommand):

    class _SnapshotSpider(scrapy.Spider):
        name = 'SnapshotResponse'
        def parse(self, response):
            GentestCommand.res = response
            GentestCommand._SnapshotSpider.callback(response)

    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def syntax(self):
        return '<url> <spider> <method>'

    def long_desc(self):
        return str(
            'Generate a test by snapshotting the url '
            'and the current results of the spider method')

    def short_desc(self):
        return 'Generate a test'

    def run(self, args, opts):
        if len(args) != 3:
            message = 'Expected 3 arguments, got {}'.format(len(args))
            raise UsageError(message, print_help = True)
        url, spider, method = args

        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            message = str(
                'The first arguments should be an url, '
                'but \'{}\' is an invalid url'
            ).format(url)
            raise UsageError(message, print_help = True)

        logger = logging.getLogger(__name__)

        def freeze(response):
            # TODO [Owlree]
            # This method should be async.
            if hasattr(catpol.spiders, spider):
                spider_object = getattr(catpol.spiders, spider)()
                if hasattr(spider_object, method):
                    spider_object_method = getattr(spider_object, method)
                    FrozenResponses.freeze_response(
                        response,
                        url,
                        spider,
                        method
                    )
                    results = list(spider_object_method(response))
                    FrozenResponses.freeze_results(results, url, spider, method)

                    # TODO [Owlree]
                    # Thes screenshot part should be factored out.
                    snap_path = FrozenResponses._directory(url, spider, method)
                    snap_complete_path = os.path.join(
                        snap_path,
                        'screenshot.png')
                    logger.info('Snapshotting {} with selenium'.format(url))
                    driver = webdriver.PhantomJS()
                    driver.set_window_size(1600, 1200)
                    driver.get(url)
                    driver.execute_script(
                        'document.body.style.background = \'white\'')
                    driver.save_screenshot(snap_complete_path)
                else:
                    message = str(
                        'The method \'{}\' does not exist in spider \'{}\''
                    ).format(method, spider)
                    raise UsageError(message, print_help = True)
            else:
                message = str(
                    'The spider \'{}\' does not be loaded'
                ).format(spider)
                raise UsageError(message, print_help = True)

        GentestCommand._SnapshotSpider.start_urls = [url]
        GentestCommand._SnapshotSpider.callback = freeze

        logger.info(
            'Unleashing spider {} on {} with method {}'.format(
                spider,
                url,
            method)
        )
        process = scrapy.crawler.CrawlerProcess()
        process.crawl(GentestCommand._SnapshotSpider)
        process.start()
