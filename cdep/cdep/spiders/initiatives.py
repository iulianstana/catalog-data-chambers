# -*- coding: utf-8 -*-
import scrapy

import cdep.loaders as loaders
import cdep.items as items

class InitiativesSpider(scrapy.Spider):
    name = 'initiatives'

    def start_requests(self):
        urls = [
            'http://www.cdep.ro/pls/parlam/structura2015.de?leg=2016'
            # 'http://www.cdep.ro/pls/parlam/structura2015.de?leg=2012'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_ids)

    def parse_ids(self, response):
        urls = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list table tbody tr td:nth-child(2) a::attr(href)').extract()

        for url in urls:
            yield scrapy.Request(url = response.urljoin(url), callback = self.parse_person)

    def parse_person(self, response):
        url = response.xpath('//a[text()=\'Initiative legislative\']/@href').extract_first()
        yield scrapy.Request(url = response.urljoin(url), callback = self.parse_initiatives)

    def parse_initiatives(self, response):
        cdep   = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(2)')
        senat  = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(3)')
        title  = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(4)')
        status = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(5)')
        author_name = response.css('div.profile-dep div.boxTitle h1::text').extract_first()

        i = 0
        while i < len(title):

            status_loader = loaders.StatusLoader(items.StatusItem())

            if cdep[i].xpath('.//a/@href').extract_first():
                status_cdep_loader = loaders.LinkLoader(items.LinkItem())
                status_cdep_loader.add_value('title', cdep[i].xpath('.//text()').extract_first())
                status_cdep_loader.add_value('href', response.urljoin(cdep[i].xpath('.//a/@href').extract_first()))
                status_loader.add_value('camera_deputatilor', status_cdep_loader.load_item())

            if senat[i].xpath('.//a/@href').extract_first():
                status_senat_loader = loaders.LinkLoader(items.LinkItem())
                status_senat_loader.add_value('title', senat[i].xpath('.//text()').extract_first())
                status_senat_loader.add_value('href', response.urljoin(senat[i].xpath('.//a/@href').extract_first()))
                status_loader.add_value('senat', status_senat_loader.load_item())

            status_loader.add_value('status', ' '.join(status[i].xpath('.//text()').extract()))

            loader = loaders.InitiativeLoader(items.InitiativeItem())
            loader.add_value('title', title[i].xpath('.//text()').extract_first())
            loader.add_value('author', author_name)
            loader.add_value('status', status_loader.load_item())
            yield loader.load_item()

            i += 1
