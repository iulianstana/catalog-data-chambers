# -*- coding: utf-8 -*-
import scrapy


class InitiativesSpider(scrapy.Spider):
    name = 'initiatives'

    def start_requests(self):
        urls = [
            'http://www.cdep.ro/pls/parlam/structura2015.de?leg=2016',
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
        dep    = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(2)')
        senat  = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(3)')
        title  = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(4)')
        status = response.css('div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr td:nth-child(5)')
        name   = response.css('div.profile-dep div.boxTitle h1::text').extract_first()

        i = 0
        while i < len(title):
            yield {
                'name': name,
                'dep': dep[i].xpath('.//text()').extract_first(),
                'senat': senat[i].xpath('.//text()').extract_first(),
                'title': title[i].xpath('.//text()').extract_first(),
                'status': status[i].xpath('.//text()').extract_first()
            }
            i += 1
