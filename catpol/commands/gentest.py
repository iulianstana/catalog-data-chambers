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
            'and the current result of the spider')

    def short_desc(self):
        return 'Generate a test'

    def run(self, args, opts):
        url, spider, method = args

        logger = logging.getLogger(__name__)

        snapshot_name = 'catpol/test/responses/frozen/{}-{}-{}'.format(
            spider,
            method,
            int(time.time())
        )

        GentestCommand._SnapshotSpider.start_urls = [url]
        GentestCommand._SnapshotSpider.output_file = snapshot_name + '.pkl'

        process = scrapy.crawler.CrawlerProcess()
        process.crawl(GentestCommand._SnapshotSpider)
        logger.info('Unleashing spider on {}'.format(url))
        process.start()

        spider_class = getattr(catpol.spiders, spider)
        spider_class_instance = spider_class()
        spider_class_instance_method = getattr(spider_class_instance, method)

        response = pickle.load(open(snapshot_name + '.pkl', 'rb'))
        result = [dict(item) for item in spider_class_instance_method(response)]

        print(result)

        with open(snapshot_name + '.json', 'w') as out:
            json.dump(result, out)

        logger.info('Snapshotting {} with selenium'.format(url))
        driver = webdriver.PhantomJS()
        driver.set_window_size(1600, 1200)
        driver.get(url)
        driver.execute_script('document.body.style.background = \'white\'')
        driver.save_screenshot(snapshot_name + '.png')
