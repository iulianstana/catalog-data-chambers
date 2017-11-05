import scrapy

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http

import catpol.cmdinput as cmdinput


class Cdep(scrapy.Spider):
    """This spider crawls for:
    - personal data
    - initiatives
    - plenery time
    """
    name = 'circ'

    def __init__(self, legs=None):
        super().__init__()
        self.legs = cmdinput.expand_legs_str(legs)

    def start_requests(self):
        for leg in self.legs:
            url = 'http://www.cdep.ro/pls/parlam/structura2015.ce?leg={leg}'.format(leg=leg)
            yield http.Reqo(url=url,
                            callback=self.follow_circs,
                            meta={'leg': leg})

    def follow_circs(self, response):
        sidebar = response.css('div.resurse-parlamentare-box')
        urls = sidebar.xpath('.//a/@href').extract()
        for url in urls:
            yield http.Reqo(url=response.urljoin(url),
                            callback=self.parse_circ,
                            meta=response.meta)

    def parse_circ(self, response):
        title = response.css('.stiri-box .program-lucru-detalii .boxTitle h1::text').extract_first()
        people = response.css('.stiri-box .program-lucru-detalii table tr')
        circ = items.CircItem()
        circ['name'] = title
        circ['url'] = response.url
        circ['leg'] = response.meta['leg']
        for p in people:
            name = p.css('td:nth-child(2) a::text').extract_first()
            href = response.urljoin(p.css('td:nth-child(2) a::attr(href)').extract_first())
            party = p.css('td:nth-child(4) a::text').extract_first()
            party_href = response.urljoin(p.css('td:nth-child(4) a::attr(href)').extract_first())
            party2 = p.css('td:nth-child(6) a::text').extract_first()
            party2_href = response.urljoin(p.css('td:nth-child(6) a::attr(href)').extract_first())

            if name is not None:
                res = {
                    'name': name,
                    'url': href,
                }
                if party is not None:
                    res['party'] = {
                        'name': party,
                        'url': party_href
                    }
                if party2 is not None:
                    res['party2'] = {
                        'name': party2,
                        'url': party2_href
                    }
                circ['people'].append(res)
        yield circ
