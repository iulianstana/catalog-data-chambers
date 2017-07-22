import json

import scrapy

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http


class EuroSpider(scrapy.Spider):

    name = 'euro'

    def start_requests(self):
        url = 'http://www.europarl.europa.eu/meps/en/json/getDistricts.html'
        yield http.Reqo(url=url, callback=self.parse_json)

    def parse_json(self, response):
        json_obj = json.loads(response.body_as_unicode())

        romania = [person for person in json_obj['result']
                                               if person['countryCode'] == 'ro']

        for dude in romania:
            url = response.urljoin(dude['detailUrl'])
            yield http.Reqo(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        personal_data_loader = loaders.PersonalDataLoader(
                                                       items.PersonalDataItem())

        name = ' '.join(response.css('.mep_name').xpath('.//text()').extract()
                                                                       ).strip()
        personal_data_loader.add_value('name', name)

        more_info = ' '.join([x.strip() for x in response.css(
                            '.more_info').xpath('.//text()').extract()]).strip()

        cln = more_info.find(':')
        cm = more_info.find(',')

        if cln >= 0 and cm >= 0:
            bday = more_info[cln + 1:cm].strip()
            personal_data_loader.add_value('birthdate', bday)

        personal_data_loader.add_value('url', response.url)

        yield personal_data_loader.load_item()
