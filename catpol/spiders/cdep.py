import scrapy
import logging

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http


class Cdep(scrapy.Spider):
    name = 'cdep'

    def __init__(self, year=None, years='', after=1990, entities='initiataives activity plenery_time'):
        logger = logging.getLogger(__name__)
        self.years = {}
        all_years = {2016, 2012, 2008, 2004, 2000, 1996, 1992, 1990}
        all_years_str = ', '.join(map(str, sorted(list(all_years))))
        if year:
            try:
                year = int(year)
                if year in all_years:
                    self.years = {int(year)}
                else:
                    logger.error(
                        str(
                            'Year {} is not valid. '
                            'Year must be one of {}.'
                        ).format(
                            year,
                            all_years_str))
            except ValueError:
                logger.error('Could not parse \'{}\' to integer.'.format(year))
        elif years:
            greater_years = {year for year in all_years if year >= int(after)}
            if years:
                arg_years = set(map(int, years.split()))
                invalid_years = sorted(list(arg_years.difference(all_years)))
                if len(invalid_years) == 0:
                    self.years = greater_years.intersection(arg_years)
                else:
                    invalid_years_str = ', '.join(map(str, invalid_years))
                    if len(invalid_years) == 1:
                        logger.error(
                            str(
                                'Year {} is not valid. '
                                'Year must be one of {}.'
                            ).format(
                                invalid_years_str,
                                all_years_str))
                    else:
                        logger.error(
                            str(
                                'Years {} are not valid. '
                                'Year must be one of {}.'
                            ).format(
                                invalid_years_str,
                                all_years_str))
        else:
            self.years = {year for year in all_years if year >= int(after)}
        entities = entities.split()
        self.should_parse_initiatives = 'initiatives' in entities
        self.should_parse_activity = 'activity' in entities
        self.should_parse_plenery_time = 'plenery_time' in entities

    def start_requests(self):
        urls = {
            'http://www.cdep.ro/pls/parlam/structura2015.de?leg={}'
            .format(year) for year in self.years
        }

        for url in urls:
            yield http.Reqo(url=url, callback=self.parse_ids)

    def parse_ids(self, response):
        urls = response.css(
            str(
                'div.grup-parlamentar-list.grupuri-parlamentare-list '
                'table tbody tr td:nth-child(2) a::attr(href)')
        ).extract()

        for url in urls:
            yield http.Reqo(
                url=response.urljoin(url),
                callback=self.parse_person)

    def parse_person(self, response):
        should_parse_activity = True
        if hasattr(self, 'should_parse_activity'):
            should_parse_activity = self.should_parse_activity
        if should_parse_activity:
            div_text = 'Activitatea parlamentara în cifre'
            activity_rows = response.xpath(
                '//text()[contains(.,\'{}\')]/../../table/tr'.format(div_text)
            )

            activity_loader = loaders.ActivityLoader(items.ActivityItem())
            activity_dict = dict()
            for row in activity_rows:
                columns = row.xpath('.//td')
                if len(columns) == 2:
                    key = ''.join(columns[0].xpath(
                        './/text()').extract()).strip(':')
                    value = ''.join(columns[1].xpath('.//text()').extract())
                    activity_dict[key] = value
            activity_loader.add_value('dictionary', activity_dict)

            person_name = response.css(
                'div.profile-dep div.boxTitle h1::text'
            ).extract_first()
            activity_loader.add_value('name', person_name)
            activity_loader.add_value('url', response.url)
            yield activity_loader.load_item()

        should_parse_initiatives = True
        if hasattr(self, 'should_parse_initiatives'):
            should_parse_initiatives = self.should_parse_initiatives

        if should_parse_initiatives:
            url = response.xpath(
                '//a[text()=\'Initiative legislative\']/@href').extract_first()
            yield http.Reqo(
                url=response.urljoin(url),
                callback=self.parse_initiatives)

        should_parse_plenery_time = True
        if hasattr(self, 'should_parse_plenery_time'):
            should_parse_plenery_time = self.should_parse_plenery_time

        if should_parse_plenery_time:
            field_name = 'Luari de cuvânt:'
            url = response.xpath(
                '//tr/td[text()=\'{}\']/following-sibling::td/a/@href'.format(field_name)).extract_first()
            yield http.Reqo(
                url=response.urljoin(url),
                callback=self.parse_plenery_time)

    def parse_initiatives(self, response):
        author_name = response.css(
            'div.profile-dep div.boxTitle h1::text'
        ).extract_first()
        rows = response.css(
            'div.grup-parlamentar-list.grupuri-parlamentare-list tbody tr')
        cdep = rows.css('td:nth-child(2)')
        senat = rows.css('td:nth-child(3)')
        title = rows.css('td:nth-child(4)')
        status = rows.css('td:nth-child(5)')
        i = 0
        while i < len(title):
            status_loader = loaders.StatusLoader(items.StatusItem())
            if cdep[i].xpath('.//a/@href').extract_first():
                status_cdep_loader = loaders.LinkLoader(items.LinkItem())
                status_cdep_loader.add_value(
                    'title',
                    cdep[i].xpath('.//text()').extract_first())
                status_cdep_loader.add_value(
                    'href',
                    response.urljoin(
                        cdep[i].xpath('.//a/@href').extract_first()))
                status_loader.add_value(
                    'cdep',
                    dict(status_cdep_loader.load_item()))
            if senat[i].xpath('.//a/@href').extract_first():
                status_senat_loader = loaders.LinkLoader(items.LinkItem())
                status_senat_loader.add_value(
                    'title',
                    senat[i].xpath('.//text()').extract_first())
                status_senat_loader.add_value(
                    'href',
                    response.urljoin(
                        senat[i].xpath('.//a/@href').extract_first()))
                status_loader.add_value(
                    'senat',
                    dict(status_senat_loader.load_item()))
            status_loader.add_value(
                'status',
                ' '.join(status[i].xpath('.//text()').extract())
            )
            loader = loaders.InitiativeLoader(items.InitiativeItem())
            loader.add_value(
                'title',
                title[i].xpath('.//text()').extract_first())
            loader.add_value('author', author_name)
            loader.add_value('status', dict(status_loader.load_item()))
            loader.add_value('url', response.url)
            yield loader.load_item()
            i += 1

    def parse_plenery_time(self, response):
        loader = loaders.PleneryTimeLoader(item=items.PleneryTimeItem(), response=response)
        loader.add_xpath('duration', '//tr/td[text()=\'total durată video:\']/following-sibling::td//text()')
        loader.add_xpath('name', '//tr/td[text()=\'vorbitor:\']/following-sibling::td//text()')
        loader.add_value('url', response.url)
        yield loader.load_item()

