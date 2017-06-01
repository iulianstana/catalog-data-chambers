import scrapy
import logging

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http

import catpol.cmdinput as cmdinput

class CdepCounties(scrapy.Spider):
    name = 'cdep_counties'

    def __init__(self, after=None, years=None):
        self.years = cmdinput.expand_years(after, years)
        print(self.years)

    def start_requests(self):
        urls = {
            'http://www.cdep.ro/pls/parlam/structura2015.ce?leg={}'
            .format(year) for year in self.years
        }
        for url in urls:
            yield http.Reqo(url=url, callback=self.parse_ids)

    def parse_ids(self, response):
        for a in response.css('div.resurse-list ul li a'):
            url = response.urljoin(a.xpath('.//@href').extract_first())
            yield http.Reqo(url=url, callback=self.parse_county)

    def parse_county(self, response):

        county_name = response.xpath('//*[contains(text(),\'Circumscriptia electorala\')]/text()').extract_first()

        # TODO This should work with tbody, but it does not. Why?
        rows = response.css(
            str(
                'div.grup-parlamentar-list.grupuri-parlamentare-list '
                'table tr')
        )
        people = []
        for row in rows:
            cell = row.css('td:nth-child(2)')
            name = cell.css('a::text').extract_first()
            if name is None:
                continue
            party = row.css('td:nth-child(4) a::text').extract_first()
            url = response.urljoin(cell.css('a::attr(href)').extract_first())
            people.append({'name': name, 'url': url, 'party': party})

        yield items.CountyItem(people=people, url=response.url, name=county_name)
