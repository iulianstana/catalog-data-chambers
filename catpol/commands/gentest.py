import os
import time
import pickle
import logging
import scrapy
import json

import catpol.spiders

from selenium import webdriver

class GentestCommand(scrapy.commands.ScrapyCommand):

    class _SnapshotSpider(scrapy.Spider):
        name = 'SnapshotResponse'
        def parse(self, response):
            with open(
                GentestCommand._SnapshotSpider.output_file, 'wb'
            ) as output:
                pickle.dump(response, output, pickle.HIGHEST_PROTOCOL)

    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def syntax(self):
        return '<url> <spider>'

    def long_desc(self):
        return str(
            'Generate a test by snapshotting the webpage '
            'and the current results of the spider')

    def short_desc(self):
        return 'Generate a test'

    def run(self, args, opts):
        url, spider, method = args

        logger = logging.getLogger(__name__)

        assert(url.find('//') <= 5)
        url_filename = url[url.find('//') + 2:].replace('/', '-')

        snapshot_name = 'catpol/test/responses/frozen/{}/{}/{}/'.format(
            spider,
            method,
            url_filename
        )

        snapshot_name_response = os.path.join(snapshot_name, 'response.pkl')
        snapshot_name_results = os.path.join(snapshot_name, 'results.pkl')
        snapshot_name_screenshot = os.path.join(snapshot_name, 'screenshot.png')

        if not os.path.exists(os.path.dirname(snapshot_name)):
            try:
                os.makedirs(os.path.dirname(snapshot_name))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        GentestCommand._SnapshotSpider.start_urls = [url]
        GentestCommand._SnapshotSpider.output_file = snapshot_name_response

        process = scrapy.crawler.CrawlerProcess()
        process.crawl(GentestCommand._SnapshotSpider)
        logger.info('Unleashing spider on {}'.format(url))
        process.start()

        spider_class = getattr(catpol.spiders, spider)
        spider_class_instance = spider_class()
        spider_class_instance_method = getattr(spider_class_instance, method)

        response = pickle.load(open(snapshot_name_response, 'rb'))
        results = list(spider_class_instance_method(response))

        with open(
            snapshot_name_results, 'wb'
        ) as output:
            pickle.dump(results, output, pickle.HIGHEST_PROTOCOL)

        logger.info('Snapshotting {} with selenium'.format(url))
        driver = webdriver.PhantomJS()
        driver.set_window_size(1600, 1200)
        driver.get(url)
        driver.execute_script('document.body.style.background = \'white\'')
        driver.save_screenshot(snapshot_name + 'screenshot.png')
